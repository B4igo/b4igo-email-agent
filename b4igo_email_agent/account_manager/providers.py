"""Provider abstraction for pulling emails from linked accounts."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from .models import LinkedAccount


class EmailProvider(ABC):
    """Interface for provider-specific email pulling logic."""

    @abstractmethod
    def pull(self, account: LinkedAccount) -> list[dict[str, Any]]:
        """Pull emails for a linked account.

        Args:
            account: Linked account with provider credentials.

        Returns:
            List of normalized email dictionaries.
        """


class ImapProvider(EmailProvider):
    """IMAP provider adapter.

    Notes:
        This preprod implementation is intentionally minimal and returns a stub
        response shape. Real IMAP fetch logic can replace this method without
        changing the AccountManager service contract.
    """

    def pull(self, account: LinkedAccount) -> list[dict[str, Any]]:
        """Pull emails through IMAP credentials for one account."""
        password = account.credentials.get("password")
        if not password:
            raise ValueError("IMAP account is missing required password credential")

        return [
            {
                "provider": "imap",
                "accountId": account.id,
                "emailAddress": account.email_address,
                "subject": "IMAP pull placeholder",
                "body": "Provider integration pending.",
                "receivedAt": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "status": "stub",
                },
            }
        ]


class GmailProvider(EmailProvider):
    """Gmail OAuth provider adapter.

    Notes:
        This preprod implementation validates OAuth token presence and returns
        a placeholder record. Another team can swap in Gmail API calls while
        keeping the same pull interface.
    """

    def pull(self, account: LinkedAccount) -> list[dict[str, Any]]:
        """Pull emails through Gmail OAuth credentials for one account."""
        has_access_token = bool(account.credentials.get("access_token"))
        has_refresh_token = bool(account.credentials.get("refresh_token"))
        if not has_access_token and not has_refresh_token:
            raise ValueError(
                "Gmail account requires access_token or refresh_token credential"
            )

        return [
            {
                "provider": "gmail",
                "accountId": account.id,
                "emailAddress": account.email_address,
                "subject": "Gmail pull placeholder",
                "body": "Provider integration pending.",
                "receivedAt": datetime.now(timezone.utc).isoformat(),
                "metadata": {
                    "status": "stub",
                },
            }
        ]
