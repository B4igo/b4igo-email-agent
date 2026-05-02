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

    def seed_user(
        self, username: str, password: str, role: str = "user"
    ) -> dict[str, Any]:
        """Create or update one user used by app-level authentication."""
        return self.storage.upsert_user(username=username, password=password, role=role)

    def authenticate_user(
        self, username: str, password: str
    ) -> Optional[dict[str, Any]]:
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
        connector_name: Optional[str] = None,
        oauth_callback_url: Optional[str] = None,
        client_secrets_file: str = "client_secrets.json",
    ) -> Optional[list[dict[str, Any]]]:
        """Return setup flow required for a provider.

        Args:
            provider: Provider name (e.g. 'gmail').
            b4igo_user_id: B4iGO user identifier.
            connector_name: Optional label for the account.
            oauth_callback_url: Deprecated. Now unused. Setup will use default backend redirect.
            client_secrets_file: Path to client secrets.

        Returns:
            List of step dictionaries, or None if unsupported provider.
        """
        adapter = self.providers.get(provider)
        if adapter is None:
            return None

        # Build backend redirect URL automatically
        # Fallback to localhost if not configured, though standard is 127.0.0.1:5100
        redirect_uri = f"http://127.0.0.1:5100/api/providers/{provider}/oauth/callback"

        steps = adapter.GetSetup(
            account_id=b4igo_user_id,
            storage=self.storage,
            client_secrets_file=client_secrets_file,
            redirect_uri=redirect_uri,
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
        steps: list[dict[str, Any]],
        b4igo_user_id: str,
    ) -> dict[str, Any]:
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
        request_args: dict[str, Any],
        client_secrets_file: str = "client_secrets.json",
    ) -> str:
        """Pass OAuth callback to the correct provider.

        Args:
            provider: The provider name.
            request_args: HTTP query parameters from the redirect.
            client_secrets_file: Path to client_secrets.json.
        """
        adapter = self.providers.get(provider)
        if adapter is None:
            return "Unsupported provider"

        # Build backend redirect URL automatically
        redirect_uri = f"http://127.0.0.1:5100/api/providers/{provider}/oauth/callback"

        # inject config for provider
        args = dict(request_args)
        args["client_secrets_file"] = client_secrets_file
        args["redirect_uri"] = redirect_uri

        return adapter.HandleCallback(args, self.storage)

    def pull(self, b4igo_user_id: str, account_ids: list[int] = []) -> dict[str, Any]:
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
