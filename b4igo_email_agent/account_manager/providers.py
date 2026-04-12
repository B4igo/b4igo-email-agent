"""Provider abstraction for pulling emails from linked accounts."""

from abc import ABC, abstractmethod
from typing import Any

from . import AccountStorage
from .models import EmailSetupStep, LinkedAccount
from datetime import datetime, timedelta, timezone
import base64
import email
import imaplib
from email.utils import parsedate_to_datetime

def _since_dt(last_read: datetime | None, fallback_days: int = 14) -> datetime:
    if last_read is not None:
        return last_read.astimezone(timezone.utc)
    return datetime.now(timezone.utc) - timedelta(days=fallback_days)

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
    def CallFunction(self, function_name: str, steps: list[EmailSetupStep], account_id: str, storage: AccountStorage) -> str:
        """Handle provider-specific setup callback hooks."""


class ImapProvider(EmailProvider):
    """IMAP provider adapter.

    Notes:
        This preprod implementation is intentionally minimal and returns a stub
        response shape. Real IMAP fetch logic can replace this method without
        changing the AccountManager service contract.
    """

    def pull(self, account: LinkedAccount) -> list[dict[str, Any]]:
        host = str(account.config.get("host", "")).strip()
        if not host:
            raise ValueError("IMAP config missing host")
        port = int(account.config.get("port", 993))
        use_ssl = bool(account.config.get("use_ssl", True))
        mailbox = str(account.config.get("mailbox", "INBOX"))

        username = account.credentials.get("username") or account.email_address
        password = account.credentials.get("password")
        if not password:
            raise ValueError("IMAP account is missing required password credential")

        since = _since_dt(account.last_read)
        since_search = since.strftime("%d-%b-%Y")

        conn = imaplib.IMAP4_SSL(host, port) if use_ssl else imaplib.IMAP4(host, port)
        try:
            conn.login(str(username), str(password))
            conn.select(mailbox)
            status, data = conn.search(None, "SINCE", since_search)
            if status != "OK" or not data or not data[0]:
                return []

            out: list[dict[str, Any]] = []
            for msg_id in data[0].split():
                f_status, msg_data = conn.fetch(msg_id, "(RFC822)")
                if f_status != "OK" or not msg_data:
                    continue
                raw_bytes = msg_data[0][1]
                msg = email.message_from_bytes(raw_bytes)

                subject = str(msg.get("Subject", ""))
                sender = str(msg.get("From", ""))
                date_raw = msg.get("Date")
                try:
                    received = parsedate_to_datetime(date_raw).astimezone(
                        timezone.utc).isoformat() if date_raw else None
                except Exception:
                    received = None

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" and "attachment" not in str(
                                part.get("Content-Disposition", "")).lower():
                            payload = part.get_payload(decode=True) or b""
                            charset = part.get_content_charset() or "utf-8"
                            body = payload.decode(charset, errors="replace")
                            break
                else:
                    payload = msg.get_payload(decode=True) or b""
                    body = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")

                out.append({
                    "provider": "imap",
                    "accountId": account.id,
                    "emailAddress": account.email_address,
                    "subject": subject,
                    "body": body,
                    "receivedAt": received or datetime.now(timezone.utc).isoformat(),
                    "metadata": {"from": sender, "mailbox": mailbox},
                })

            return out
        finally:
            try:
                conn.logout()
            except Exception:
                pass

    def GetSetup(self) -> list[EmailSetupStep]:
        return [
            EmailSetupStep(
                title="Email address",
                desc="Full IMAP account email (e.g. user@example.com)",
                type="input",
            ),
            EmailSetupStep(
                title="IMAP host",
                desc="e.g. imap.example.com",
                type="input",
                value="",
            ),
            EmailSetupStep(
                title="IMAP port",
                desc="993 for SSL, 143 for plaintext/starttls environments",
                type="input",
                value="993",
            ),
            EmailSetupStep(
                title="Use SSL",
                desc="true/false",
                type="boolean",
                value="true",
            ),
            EmailSetupStep(
                title="Username (optional)",
                desc="Leave blank to use email address",
                type="input",
                value="",
            ),
            EmailSetupStep(
                title="Password / app password",
                desc="",
                type="password",
                callback="final_step",
            ),
        ]

    def CallFunction(self, function_name: str, steps: list[EmailSetupStep], account_id: str, storage: AccountStorage) -> str:
        """Handle provider-specific setup callback hooks with user context for connector creation."""
        if function_name != "final_step":
            raise ValueError(f"Unknown function name: {function_name}")

        try:
            email_address = (steps[0].value or "").strip()
            host = (steps[1].value or "").strip()
            port = int((steps[2].value or "993").strip())
            use_ssl = str(steps[3].value or "true").strip().lower() in ("1", "true", "yes", "on")
            username = (steps[4].value or "").strip() or email_address
            password = (steps[5].value or "").strip()

            if not email_address or not host or not username or not password:
                return "Missing required IMAP fields"

            # First validate the connection
            conn = imaplib.IMAP4_SSL(host, port) if use_ssl else imaplib.IMAP4(host, port)
            try:
                conn.login(username, password)
                status, _ = conn.select("INBOX")
                if status != "OK":
                    return "IMAP login worked but INBOX could not be selected"
            finally:
                try:
                    conn.logout()
                except Exception:
                    pass

            # Connection validated, now create the connector if user context is available
            if account_id and storage:
                config = {
                    "host": host,
                    "port": port,
                    "use_ssl": use_ssl,
                    "mailbox": "INBOX"
                }

                credentials = {
                    "username": username,
                    "password": password
                }

                account = storage.upsert_account(
                    b4igo_user_id=account_id,
                    provider="imap",
                    email_address=email_address,
                    credentials=credentials,
                    display_name=email_address,
                    config=config,
                )

                if account is None: return "Failed to create IMAP connector"
            else: return "User context not available for connector creation"

            return ""
        except Exception as exc:
            return f"IMAP validation failed: {exc}"


class GmailProvider(EmailProvider):
    """Gmail OAuth provider adapter.

    Notes:
        This preprod implementation validates OAuth token presence and returns
        a placeholder record. Another team can swap in Gmail API calls while
        keeping the same pull interface.
    """
    def pull(self, account: LinkedAccount) -> list[dict[str, Any]]:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        token = account.credentials.get("token") or account.credentials.get("access_token")
        refresh_token = account.credentials.get("refresh_token")
        if not token and not refresh_token:
            raise ValueError("Gmail account requires token/access_token or refresh_token")

        creds = Credentials(
            token=token,
            refresh_token=refresh_token,
            token_uri=account.credentials.get("token_uri"),
            client_id=account.credentials.get("client_id"),
            client_secret=account.credentials.get("client_secret"),
            scopes=account.credentials.get("scopes"),
        )
        service = build("gmail", "v1", credentials=creds)

        since = _since_dt(account.last_read)
        query = f"after:{int(since.timestamp())}"
        max_results = int(account.config.get("max_results", 50))

        listed = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results,
        ).execute()

        messages = listed.get("messages", [])
        out: list[dict[str, Any]] = []
        for m in messages:
            full = service.users().messages().get(
                userId="me", id=m["id"], format="full"
            ).execute()

            headers = {
                h.get("name", "").lower(): h.get("value", "")
                for h in full.get("payload", {}).get("headers", [])
            }

            subject = headers.get("subject", "")
            sender = headers.get("from", "")
            internal_ms = int(full.get("internalDate", "0") or 0)
            received_at = (
                datetime.fromtimestamp(internal_ms / 1000, tz=timezone.utc).isoformat()
                if internal_ms > 0
                else datetime.now(timezone.utc).isoformat()
            )

            snippet = full.get("snippet", "")

            out.append({
                "provider": "gmail",
                "accountId": account.id,
                "emailAddress": account.email_address,
                "subject": subject,
                "body": snippet,
                "receivedAt": received_at,
                "metadata": {"from": sender, "gmailMessageId": full.get("id")},
            })


        return out

    def GetSetup(self) -> list[EmailSetupStep]:
        """Describe one redirect step for Gmail OAuth linking."""
        return [
            EmailSetupStep(
                title="Continue to Gmail login and authorization",
                desc="You will be redirected to Google to grant read access to B4iGO.",
                type="redirect",
                callback="start_oauth",
            )
        ]

    def CallFunction(self, function_name: str, steps: list[EmailSetupStep], account_id: str, storage: AccountStorage) -> str:
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
