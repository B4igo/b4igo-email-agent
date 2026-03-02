"""Application service for linked account management and provider pulls."""

from typing import Any, Optional

from .models import ProviderType
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

    def list_accounts(self, b4igo_user_id: str) -> list[dict[str, Any]]:
        """List all linked accounts for a user."""
        accounts = self.storage.list_accounts(b4igo_user_id)
        return [account.to_public_dict() for account in accounts]

    def delete_account(self, b4igo_user_id: str, account_id: int) -> bool:
        """Delete one linked account for a user."""
        return self.storage.delete_account(b4igo_user_id, account_id)

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
                emails.extend(provider.pull(account))
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
