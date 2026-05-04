"""Application service for linked account management and provider pulls."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from .models import EmailSetupStep, ProviderType
from .providers import EmailProvider, GmailProvider, ImapProvider
from .storage import AccountStorage
import httpx
import os
import jwt
import logging

logger = logging.getLogger(__name__)

class SIWEClient:
    """Client for SIWE GraphQL server."""

    def __init__(self, url: Optional[str] = None):
        self.url = url or os.environ.get("B4IGO_BACKEND_GRAPHQL_URL", "")

        if not self.url:
            raise ValueError("B4IGO_BACKEND_GRAPHQL_URL environment variable is not set")

        if self.url:
            self.url = self.url.rstrip("/")

    def init_siwe(self, address: str) -> dict[str, Any]:
        """Execute HelloServer mutation."""
        query = '''
        mutation HelloServer($input: SiweHelloRequestInput!) {
          HelloServer(input: $input) {
            siweMessage
            requestId
          }
        }
        '''
        variables = {"input": {"address": address}}
        try:
            headers = {
                "Accept": "application/json",
                "User-Agent": "B4iGO-AccountManager/1.0"
            }
            response = httpx.post(self.url, json={"query": query, "variables": variables}, headers=headers, timeout=30)

            if response.status_code != 200:
                response.raise_for_status()

            if not response.text.strip():
                logger.error("SIWEClient: init_siwe returned empty body")
                return {}

            try:
                data = response.json()
            except Exception as je:
                logger.error("SIWEClient: init_siwe JSON decode failed. Content-Type: %s, Body: %s",
                             response.headers.get("Content-Type"), response.text[:500])
                raise je

            return data.get("data", {}).get("HelloServer", {})
        except Exception as e:
            logger.error("SIWEClient: init_siwe failed: %s", e)
            raise

    def verify_siwe(self, signature: str, request_id: str) -> dict[str, Any]:
        """Execute VerifySignature mutation."""
        query = '''
        mutation VerifySignature($input: VerifySignatureRequestInput!) {
          VerifySignature(input: $input) {
            jwt
            userId
            email
          }
        }
        '''
        variables = {"input": {"signature": signature, "requestId": request_id}}
        try:
            headers = {
                "Accept": "application/json",
                "User-Agent": "B4iGO-AccountManager/1.0"
            }
            response = httpx.post(self.url, json={"query": query, "variables": variables}, headers=headers, timeout=30)

            if response.status_code != 200:
                logger.error("SIWEClient: verify_siwe failed with status %s: %s", response.status_code, response.text)
                response.raise_for_status()

            if not response.text.strip():
                logger.error("SIWEClient: verify_siwe returned empty body")
                return {}

            try:
                data = response.json()
            except Exception as je:
                logger.error("SIWEClient: verify_siwe JSON decode failed. Content-Type: %s, Body: %s",
                             response.headers.get("Content-Type"), response.text[:500])
                raise je

            return data.get("data", {}).get("VerifySignature", {})
        except Exception as e:
            logger.error("SIWEClient: verify_siwe failed: %s", e)
            raise

    def validate_jwt(self, token: str) -> dict[str, Any]:
        """Execute GetB4igoProfile query using the Bearer token."""
        try:
            raw_token = token.split(" ")[1] if "Bearer" in token else token
            payload = jwt.decode(raw_token, options={"verify_signature": False})
            user_id = payload.get("userId") or payload.get("sub") or payload.get("id")
        except Exception:
            return {"valid": False, "error": "Invalid token format"}

        if not user_id:
            return {"valid": False, "error": "Could not extract user ID from token"}

        query = '''
        query getB4igoProfile($userId: String!) {
          getB4igoProfile(userId: $userId) {
            success
            data {
              id
            }
          }
        }
        '''
        variables = {"userId": str(user_id)}
        headers = {
            "Authorization": f"Bearer {raw_token}",
            "Accept": "application/json",
            "User-Agent": "B4iGO-AccountManager/1.0"
        }

        try:
            response = httpx.post(self.url, json={"query": query, "variables": variables}, headers=headers, timeout=30)

            if response.status_code != 200:
                logger.error("SIWEClient: validate_jwt failed with status %s: %s", response.status_code, response.text)
                return {"valid": False, "error": f"returned status {response.status_code}"}

            if not response.text.strip():
                logger.error("SIWEClient: validate_jwt returned empty body")
                return {"valid": False, "error": "returned empty body"}

            try:
                data = response.json()
            except Exception as je:
                logger.error("SIWEClient: validate_jwt JSON decode failed. Content-Type: %s, Body: %s",
                             response.headers.get("Content-Type"), response.text[:500])
                return {"valid": False, "error": "Invalid JSON response from"}

            profile = data.get("data", {}).get("getB4igoProfile", {})
            if profile.get("success") is True:
                return {"valid": True, "userId": user_id}
            return {"valid": False, "error": "Token not valid against endpoint"}
        except Exception as e:
            return {"valid": False, "error": str(e)}


class AccountManagerService:
    """Service that orchestrates account storage and provider pulls."""

    def __init__(
        self,
        storage: Optional[AccountStorage] = None,
        providers: Optional[dict[str, EmailProvider]] = None,
        siwe_client: Optional[SIWEClient] = None,
    ):
        """Initialize service dependencies.

        Args:
            storage: Storage adapter for linked accounts.
            providers: Provider registry by provider type.
            siwe_client: Client for SIWE functionality
        """
        self.storage = storage or AccountStorage()
        self.providers: dict[str, EmailProvider] = providers or {
            "imap": ImapProvider(),
            "gmail": GmailProvider(),
        }
        self.siwe_client = siwe_client or SIWEClient()

    def init_siwe(self, address: str) -> dict[str, Any]:
        """Proxy init SIWE."""
        return self.siwe_client.init_siwe(address)

    def verify_siwe(self, signature: str, request_id: str) -> dict[str, Any]:
        """Proxy verify SIWE and create user."""
        result = self.siwe_client.verify_siwe(signature, request_id)
        user_id = result.get("userId")
        if user_id:
            self.storage.upsert_user(user_id=user_id, role="user")
        return result

    def validate_token(self, token: str) -> dict[str, Any]:
        """Proxy validate JWT, and save user_id if valid."""
        result = self.siwe_client.validate_jwt(token)
        if result.get("valid") and result.get("userId"):
            self.storage.upsert_user(user_id=result.get("userId"), role="user")
        return result

    def _notify_scheduler(self, b4igo_user_id: str, account_id: int):
        """Notify scheduler to register one account for polling."""
        scheduler_url = os.environ.get("B4IGO_SCHEDULER_URL")
        if not scheduler_url:
            logger.warning("B4IGO_SCHEDULER_URL not set; skipping scheduler notification")
            return

        url = f"{scheduler_url.rstrip('/')}/api/scheduler/registry"
        try:
            httpx.post(
                url,
                json={"b4igoUserId": b4igo_user_id, "accountId": account_id},
                timeout=5
            )
            logger.info("Notified scheduler for account %d", account_id)
        except Exception as e:
            logger.error("Failed to notify scheduler for account %d: %s", account_id, e)

    def link_account(
        self,
        b4igo_user_id: str,
        provider: ProviderType,
        email_address: str,
        credentials: Dict[str, Any],
        display_name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create or update one linked account for the user."""
        account = self.storage.upsert_account(
            b4igo_user_id=b4igo_user_id,
            provider=provider,
            email_address=email_address,
            credentials=credentials,
            display_name=display_name,
            config=config,
        )
        if account is None:
            return None
        
        # Notify scheduler
        self._notify_scheduler(b4igo_user_id, account.id)
        
        return account.to_public_dict()

    def list_accounts(self, b4igo_user_id: str) -> List[Dict[str, Any]]:
        """List all linked accounts for a user."""
        accounts = self.storage.list_accounts(b4igo_user_id)
        return [account.to_public_dict() for account in accounts]

    def delete_account(self, b4igo_user_id: str, account_id: int) -> bool:
        """Delete one linked account for a user."""
        return self.storage.delete_account(b4igo_user_id, account_id)

    def list_provider_types(self) -> list[str]:
        """Return registered provider types used by setup UI."""
        return list(self.providers.keys())

    def get_provider_setup_steps(
        self,
        provider: str,
        b4igo_user_id: str,
        connector_name: Optional[str] = None,
        oauth_callback_url: Optional[str] = None,
        client_secrets_file: str = "client_secrets.json",
    ) -> Optional[List[Dict[str, Any]]]:
        """Return setup flow required for a provider.

        Args:
            provider: Provider name (e.g. 'gmail').
            b4igo_user_id: B4iGO user identifier.
            connector_name: Optional label for the account.
            oauth_callback_url: Optional override for the OAuth redirect URI.
            client_secrets_file: Path to client secrets.

        Returns:
            List of step dictionaries, or None if unsupported provider.
        """
        adapter = self.providers.get(provider)
        if adapter is None:
            return None

        # Build default redirect URL if none provided
        if not oauth_callback_url:
            am_public_url = os.environ.get("B4IGO_ACCOUNT_MANAGER_PUBLIC_URL", "http://127.0.0.1:5100")
            oauth_callback_url = f"{am_public_url.rstrip('/')}/api/providers/{provider}/oauth/callback"

        steps = adapter.GetSetup(
            account_id=b4igo_user_id,
            storage=self.storage,
            client_secrets_file=client_secrets_file,
            redirect_uri=oauth_callback_url,
            connector_name=connector_name,
        )

        return [
            {
                "title": s.title,
                "desc": s.desc,
                "type": s.type,
                "value": s.value,
                "callback": s.callback,
                "polling_id": s.polling_id,
            }
            for s in steps
            if s.type in ("redirect", "boolean", "input", "password")
        ]

    def run_provider_setup_callback(
        self,
        provider: str,
        function_name: str,
        steps: List[Dict[str, Any]],
        b4igo_user_id: str,
    ) -> Dict[str, Any]:
        """Validate setup steps by count/type and dispatch provider callback."""
        provider_adapter = self.providers.get(provider)
        if provider_adapter is None:
            return {"success": False, "message": "Unsupported provider"}

        expected_steps = provider_adapter.GetSetup()
        if len(steps) != len(expected_steps):
            return {"success": False, "message": "Validation error"}

        validated_steps: list[EmailSetupStep] = []
        for index, expected in enumerate(expected_steps):
            raw = steps[index]
            if not isinstance(raw, dict) or raw.get("type") != expected.type:
                return {"success": False, "message": "Validation error"}

            value = raw.get("value")
            validated_steps.append(
                EmailSetupStep(
                    title=str(raw.get("title", expected.title)),
                    desc=str(raw.get("desc", expected.desc)),
                    type=expected.type,
                    value=str(value) if value is not None else None,
                    callback=raw.get("callback"),
                )
            )

        try:
            message = provider_adapter.CallFunction(
                function_name, validated_steps, b4igo_user_id, self.storage
            )
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}

        if message:
            return {"success": False, "message": message}
        return {"success": True, "message": "ok"}

    def handle_oauth_callback(
        self,
        provider: str,
        request_args: Dict[str, Any],
        client_secrets_file: str = "client_secrets.json",
        redirect_uri: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Pass OAuth callback to the correct provider.

        Args:
            provider: The provider name.
            request_args: HTTP query parameters from the redirect.
            client_secrets_file: Path to client_secrets.json.
            redirect_uri: The original redirect URI used for the flow.
        """
        adapter = self.providers.get(provider)
        if adapter is None:
            return {"success": False, "error": "Unsupported provider"}

        # Build default redirect URL if none provided
        if not redirect_uri:
            am_public_url = os.environ.get("B4IGO_ACCOUNT_MANAGER_PUBLIC_URL", "http://127.0.0.1:5100")
            redirect_uri = f"{am_public_url.rstrip('/')}/api/providers/{provider}/oauth/callback"

        # inject config for provider
        args = dict(request_args)
        args["client_secrets_file"] = client_secrets_file
        args["redirect_uri"] = redirect_uri

        result = adapter.HandleCallback(args, self.storage)
        
        if isinstance(result, dict) and result.get("success"):
            account_id = result.get("accountId")
            b4igo_user_id = result.get("b4igoUserId")
            if account_id and b4igo_user_id:
                self._notify_scheduler(b4igo_user_id, account_id)
            return result
        
        if isinstance(result, str):
            if not result: # Success
                 return {"success": True}
            return {"success": False, "error": result}
            
        return result

    def pull(self, b4igo_user_id: str, account_ids: List[int] = []) -> Dict[str, Any]:
        """Pull new emails for valid linked accounts.

        Args:
            b4igo_user_id: B4iGO user identifier.
            account_ids: Optional subset of account ids to poll.

        Returns:
            Dictionary with normalized emails and per-account errors.
        """
        accounts = self.storage.get_accounts_by_ids(b4igo_user_id, account_ids or [])
        emails: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []

        for account in accounts:
            provider = self.providers.get(account.provider)
            if provider is None:
                errors.append(
                    {
                        "accountId": account.id,
                        "provider": account.provider,
                        "error": "No provider adapter registered",
                    }
                )
                continue

            try:
                last_pull = datetime.now(timezone.utc)
                emails.extend(provider.pull(account))
                self.storage.update_last_read(account.id, last_pull)
            except Exception as exc:
                errors.append(
                    {
                        "accountId": account.id,
                        "provider": account.provider,
                        "error": str(exc),
                    }
                )

        return {
            "b4igoUserId": b4igo_user_id,
            "accountsPolled": len(accounts),
            "emails": emails,
            "errors": errors,
        }
