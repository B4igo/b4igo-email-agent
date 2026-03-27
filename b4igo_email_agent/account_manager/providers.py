"""Provider abstraction for pulling emails from linked accounts."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from .models import EmailSetupStep, LinkedAccount


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

    @abstractmethod
    def GetSetup(self) -> list[EmailSetupStep]:
        """Return generic setup steps for this provider."""

    @abstractmethod
    def CallFunction(self, function_name: str, steps: list[EmailSetupStep]) -> str:
        """Handle provider-specific setup callback hooks."""


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

    def GetSetup(self) -> list[EmailSetupStep]:
        """Describe generic IMAP setup fields for the UI."""
        return [
            EmailSetupStep(
                title="Enter the IMAP email address",
                desc="Used to identify the account you want to link.",
                type="input",
            ),
            EmailSetupStep(
                title="Enter the IMAP account password",
                desc="Stored securely and used to pull mailbox data.",
                type="password",
                callback="final_step",
            ),
        ]

    def CallFunction(self, function_name: str, steps: list[EmailSetupStep]) -> str:
        """IMAP callback functions. These are callbacks for the steps.
         This function should return nothing on success and a string for any error to display on the UI.
         """
        if function_name == "final_step":
            return "IMAP linking is not implemented yet."
        raise ValueError(f"Unknown function name: {function_name}")


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

    def GetSetup(self) -> list[EmailSetupStep]:
        """Describe one redirect step for Gmail OAuth linking."""
        return [
            EmailSetupStep(
                title="Continue to Gmail login and authorization",
                desc="You will be redirected to Google to grant mailbox access.",
                type="redirect",
                callback="start_oauth",
            )
        ]

    def CallFunction(self, function_name: str, steps: list[EmailSetupStep]) -> str:
        """Validate supported callback hooks for generic setup orchestration."""
        if function_name == "start_oauth":
            return ""
        raise ValueError(f"Unknown function name: {function_name}")

    def get_authorization_url(
        self,
        client_secrets_file: str,
        redirect_uri: str,
    ) -> tuple[str, str, str]:
        """Create Gmail OAuth URL and return URL/state/PKCE verifier."""
        from google_auth_oauthlib.flow import Flow

        flow = Flow.from_client_secrets_file(
            client_secrets_file,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            redirect_uri=redirect_uri,
        )

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        return authorization_url, state, flow.code_verifier

    def exchange_code(
        self,
        auth_code: str,
        client_secrets_file: str,
        redirect_uri: str,
        state: str,
        code_verifier: str,
    ) -> dict[str, Any]:
        """Exchange OAuth code for a serializable Gmail credential payload."""
        from google_auth_oauthlib.flow import Flow

        flow = Flow.from_client_secrets_file(
            client_secrets_file,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            redirect_uri=redirect_uri,
            state=state,
        )
        flow.code_verifier = code_verifier
        flow.fetch_token(code=auth_code)
        creds = flow.credentials

        return {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }

    def get_user_email(self, credentials: dict[str, Any]) -> str:
        """Resolve Gmail account email address from OAuth credentials."""
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        creds = Credentials(
            token=credentials.get("token"),
            refresh_token=credentials.get("refresh_token"),
            token_uri=credentials.get("token_uri"),
            client_id=credentials.get("client_id"),
            client_secret=credentials.get("client_secret"),
            scopes=credentials.get("scopes"),
        )

        service = build("gmail", "v1", credentials=creds)
        profile = service.users().getProfile(userId="me").execute()
        return str(profile["emailAddress"])
