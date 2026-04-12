"""Application service for linked account management and provider pulls."""

from datetime import datetime, timezone
from typing import Any, Optional

from .models import EmailSetupStep, ProviderType
from .providers import EmailProvider, GmailProvider, ImapProvider
from .storage import AccountStorage

class AccountManagerService:
    """Service that orchestrates account storage and provider pulls."""

    def __init__(
        self,
        storage: Optional[AccountStorage] = None,
        providers: Optional[dict[ProviderType, EmailProvider]] = None,
    ):
        """Initialize service dependencies.

        Args:
            storage: Storage adapter for linked accounts.
            providers: Provider registry by provider type.
        """
        self.storage = storage or AccountStorage()
        self.providers = providers or {
            "imap": ImapProvider(),
            "gmail": GmailProvider(),
        }

    def link_account(
        self,
        b4igo_user_id: str,
        provider: ProviderType,
        email_address: str,
        credentials: dict[str, Any],
        display_name: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
    ) -> Optional[dict[str, Any]]:
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
        return account.to_public_dict()

    def seed_user(self, username: str, password: str, role: str = "user") -> dict[str, Any]:
        """Create or update one user used by app-level authentication."""
        return self.storage.upsert_user(username=username, password=password, role=role)

    def authenticate_user(self, username: str, password: str) -> Optional[dict[str, Any]]:
        """Return user profile when username/password matches, else None."""
        user = self.storage.get_user(username)
        if user is None or user.get("password") != password:
            return None
        return {
            "username": str(user["username"]),
            "role": str(user["role"]),
        }

    def user_exists(self, username: str) -> bool:
        """Return whether a username exists in auth storage."""
        return self.storage.user_exists(username)

    def list_accounts(self, b4igo_user_id: str) -> list[dict[str, Any]]:
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
        oauth_callback_url: str,
        client_secrets_file: str,
        connector_name: Optional[str] = None,
    ) -> Optional[list[dict[str, Any]]]:
        """Return setup steps for provider, filling OAuth redirect URLs when needed."""
        provider_adapter = self.providers.get(provider)
        if provider_adapter is None:
            return None

        setup_steps = provider_adapter.GetSetup()
        resolved_steps: list[EmailSetupStep] = []
        for step in setup_steps:
            resolved = EmailSetupStep(
                title=step.title,
                desc=step.desc,
                type=step.type,
                value=step.value,
                callback=step.callback,
            )

            # OAuth setup is backend-only and uses a full callback URL.
            if (
                provider == "gmail"
                and isinstance(provider_adapter, GmailProvider)
                and resolved.type == "redirect"
                and resolved.callback == "start_oauth"
            ):
                authorization_url, state, code_verifier = (
                    provider_adapter.get_authorization_url(
                        client_secrets_file=client_secrets_file,
                        redirect_uri=oauth_callback_url,
                    )
                )
                self.storage.save_gmail_oauth_session(
                    state=state,
                    b4igo_user_id=b4igo_user_id,
                    code_verifier=code_verifier,
                    connector_name=connector_name,
                )
                resolved.value = authorization_url
                resolved.callback = oauth_callback_url

            resolved_steps.append(resolved)

        return [step.__dict__ for step in resolved_steps]

    def run_provider_setup_callback(
        self,
        provider: str,
        function_name: str,
        steps_payload: list[dict[str, Any]],
        b4igo_user_id: str,
    ) -> dict[str, Any]:
        """Validate setup steps by count/type and dispatch provider callback."""
        provider_adapter = self.providers.get(provider)
        if provider_adapter is None:
            return {"success": False, "message": "Unsupported provider"}

        expected_steps = provider_adapter.GetSetup()
        if len(steps_payload) != len(expected_steps):
            return {"success": False, "message": "Validation error"}

        validated_steps: list[EmailSetupStep] = []
        for index, expected in enumerate(expected_steps):
            raw = steps_payload[index]
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
            message = provider_adapter.CallFunction(function_name, validated_steps, b4igo_user_id, self.storage)
        except Exception:
            return {"success": False, "message": "Validation error"}

        if message:
            return {"success": False, "message": message}
        return {"success": True, "message": "ok"}

    def start_gmail_oauth(
        self,
        b4igo_user_id: str,
        client_secrets_file: str,
        redirect_uri: str,
        connector_name: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create Gmail OAuth URL and persist callback state context."""
        provider = self.providers.get("gmail")
        if not isinstance(provider, GmailProvider):
            raise ValueError("Gmail provider is not registered")

        authorization_url, state, code_verifier = provider.get_authorization_url(
            client_secrets_file=client_secrets_file,
            redirect_uri=redirect_uri,
        )
        self.storage.save_gmail_oauth_session(
            state=state,
            b4igo_user_id=b4igo_user_id,
            code_verifier=code_verifier,
            connector_name=connector_name,
        )
        return {
            "authorizationUrl": authorization_url,
            "state": state,
        }

    def complete_gmail_oauth(
        self,
        auth_code: str,
        state: str,
        client_secrets_file: str,
        redirect_uri: str,
    ) -> Optional[dict[str, Any]]:
        """Complete Gmail OAuth callback and upsert linked account."""
        provider = self.providers.get("gmail")
        if not isinstance(provider, GmailProvider):
            raise ValueError("Gmail provider is not registered")

        session = self.storage.pop_gmail_oauth_session(state)
        if session is None:
            return None

        credentials = provider.exchange_code(
            auth_code=auth_code,
            client_secrets_file=client_secrets_file,
            redirect_uri=redirect_uri,
            state=state,
            code_verifier=session.code_verifier,
        )
        email_address = provider.get_user_email(credentials)

        account = self.storage.upsert_account(
            b4igo_user_id=session.b4igo_user_id,
            provider="gmail",
            email_address=email_address,
            credentials=credentials,
            display_name=session.connector_name,
            config=None,
        )
        if account is None:
            return None
        return account.to_public_dict()

    def complete_provider_oauth(
        self,
        provider: str,
        auth_code: str,
        state: str,
        client_secrets_file: str,
        redirect_uri: str,
    ) -> Optional[dict[str, Any]]:
        """Complete OAuth callback for provider types that support backend OAuth."""
        if provider == "gmail":
            return self.complete_gmail_oauth(
                auth_code=auth_code,
                state=state,
                client_secrets_file=client_secrets_file,
                redirect_uri=redirect_uri,
            )
        return None

    def pull(
        self,
        b4igo_user_id: str,
        account_ids: Optional[list[int]] = None,
    ) -> dict[str, Any]:
        """Pull emails across linked providers for a given user.

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
