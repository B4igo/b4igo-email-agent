"""Provider abstraction for pulling emails from linked accounts."""

import base64
import email
import imaplib
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from email.message import Message
from email.utils import parsedate_to_datetime
from typing import Any, Optional

from .models import EmailSetupStep, LinkedAccount
from .storage import AccountStorage


def _extract_body_and_attachments(msg: Message) -> tuple[str, list[dict[str, Any]]]:
    """Walk a parsed email and split it into a plain-text body plus attachments.

    Body is the first non-attachment text/plain part encountered. Attachments
    are any leaf part with Content-Disposition: attachment OR a non-text part
    that carries a filename. Attachment bytes are base64-encoded so the
    resulting dict survives JSON serialization (the scheduler queues these
    through Redis and forwards them to the AI service as multipart files).
    """
    body = ""
    attachments: list[dict[str, Any]] = []
    for part in msg.walk():
        if part.is_multipart():
            continue
        payload = part.get_payload(decode=True)
        if not isinstance(payload, (bytes, bytearray)):
            continue
        disposition = str(part.get("Content-Disposition", "")).lower()
        is_attachment = "attachment" in disposition
        filename = part.get_filename()
        content_type = part.get_content_type()

        if is_attachment or (filename and not content_type.startswith("text/")):
            attachments.append(
                {
                    "filename": filename or "attachment",
                    "content_type": content_type,
                    "content_b64": base64.b64encode(bytes(payload)).decode("ascii"),
                }
            )
        elif content_type == "text/plain" and not body:
            charset = part.get_content_charset() or "utf-8"
            body = bytes(payload).decode(charset, errors="replace")
    return body, attachments


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
    def GetSetup(self, **kwargs: Any) -> list[EmailSetupStep]:
        """Return generic setup steps for this provider."""

    @abstractmethod
    def CallFunction(
        self,
        function_name: str,
        steps: list[EmailSetupStep],
        account_id: str,
        storage: AccountStorage,
    ) -> str:
        """Handle provider-specific setup callback hooks."""

    def HandleCallback(
        self, request_args: dict[str, Any], storage: AccountStorage
    ) -> str:
        """Handle OAuth callback or similar external provider redirect hooks.

        By default, does nothing and raises NotImplementedError.
        """
        raise NotImplementedError


class ImapProvider(EmailProvider):
    """IMAP provider adapter.

    Notes:
        This preprod implementation is intentionally minimal and returns a stub
        response shape. Real IMAP fetch logic can replace this method without
        changing the AccountManager service contract.
    """

    def pull(self, account: LinkedAccount) -> list[dict[str, Any]]:
        """Fetch unseen messages and mark them seen on the IMAP server."""
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

        conn = imaplib.IMAP4_SSL(host, port) if use_ssl else imaplib.IMAP4(host, port)
        try:
            conn.login(str(username), str(password))
            # Select with no readonly so we can mark messages as \Seen after pulling.
            conn.select(mailbox)
            # UNSEEN is the dedup mechanism: once we mark a message \Seen below,
            # the next poll will not return it. This is robust to clock skew and
            # missing Date headers, unlike SINCE which has date-only granularity.
            status, data = conn.search(None, "UNSEEN")
            if status != "OK" or not data or not data[0]:
                return []

            out: list[dict[str, Any]] = []
            for msg_id in data[0].split():
                f_status, msg_data = conn.fetch(msg_id, "(RFC822)")
                if f_status != "OK" or not msg_data:
                    continue
                # imaplib's fetch result is a list of either tuple[bytes, bytes]
                # or bare bytes; only the tuple case carries the message body.
                first = msg_data[0]
                if not isinstance(first, tuple) or len(first) < 2:
                    continue
                raw_bytes = first[1]
                if not isinstance(raw_bytes, (bytes, bytearray)):
                    continue
                msg = email.message_from_bytes(raw_bytes)

                subject = str(msg.get("Subject", ""))
                sender = str(msg.get("From", ""))
                date_raw = msg.get("Date")
                try:
                    received = (
                        parsedate_to_datetime(date_raw)
                        .astimezone(timezone.utc)
                        .isoformat()
                        if date_raw
                        else None
                    )
                except Exception:
                    received = None

                body, attachments = _extract_body_and_attachments(msg)

                out.append(
                    {
                        "provider": "imap",
                        "accountId": account.id,
                        "emailAddress": account.email_address,
                        "subject": subject,
                        "body": body,
                        "receivedAt": received
                        or datetime.now(timezone.utc).isoformat(),
                        "metadata": {"from": sender, "mailbox": mailbox},
                        "attachments": attachments,
                    }
                )

                # Mark as seen only after we have successfully captured the message.
                # If we crash before this, the next poll will retry the same message.
                conn.store(msg_id, "+FLAGS", "\\Seen")

            return out
        finally:
            try:
                conn.logout()
            except Exception:
                pass

    def GetSetup(self, **kwargs: Any) -> list[EmailSetupStep]:
        """Return the redirect step a user must follow to link this provider."""
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

    def CallFunction(
        self,
        function_name: str,
        steps: list[EmailSetupStep],
        account_id: str,
        storage: AccountStorage,
    ) -> str:
        """Handle provider setup callbacks and create the connector for the user."""
        if function_name != "final_step":
            raise ValueError(f"Unknown function name: {function_name}")

        try:
            email_address = (steps[0].value or "").strip()
            host = (steps[1].value or "").strip()
            port = int((steps[2].value or "993").strip())
            use_ssl = str(steps[3].value or "true").strip().lower() in (
                "1",
                "true",
                "yes",
                "on",
            )
            username = (steps[4].value or "").strip() or email_address
            password = (steps[5].value or "").strip()

            if not email_address or not host or not username or not password:
                return "Missing required IMAP fields"

            # First validate the connection
            conn = (
                imaplib.IMAP4_SSL(host, port) if use_ssl else imaplib.IMAP4(host, port)
            )
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

            # Connection validated; create the connector if user context exists
            if account_id and storage:
                config = {
                    "host": host,
                    "port": port,
                    "use_ssl": use_ssl,
                    "mailbox": "INBOX",
                }

                credentials = {"username": username, "password": password}

                account = storage.upsert_account(
                    b4igo_user_id=account_id,
                    provider="imap",
                    email_address=email_address,
                    credentials=credentials,
                    display_name=email_address,
                    config=config,
                )

                if account is None:
                    return "Failed to create IMAP connector"
            else:
                return "User context not available for connector creation"

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
        """Fetch unseen messages and mark them seen on the IMAP server."""
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        token = account.credentials.get("token") or account.credentials.get(
            "access_token"
        )
        refresh_token = account.credentials.get("refresh_token")
        if not token and not refresh_token:
            raise ValueError(
                "Gmail account requires token/access_token or refresh_token"
            )

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

        listed = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=max_results,
            )
            .execute()
        )

        messages = listed.get("messages", [])
        out: list[dict[str, Any]] = []
        for m in messages:
            full = (
                service.users()
                .messages()
                .get(userId="me", id=m["id"], format="full")
                .execute()
            )

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

            out.append(
                {
                    "provider": "gmail",
                    "accountId": account.id,
                    "emailAddress": account.email_address,
                    "subject": subject,
                    "body": snippet,
                    "receivedAt": received_at,
                    "metadata": {"from": sender, "gmailMessageId": full.get("id")},
                }
            )

        return out

    def GetSetup(self, **kwargs: Any) -> list[EmailSetupStep]:
        """Describe one redirect step for Gmail OAuth linking."""
        account_id = kwargs.get("account_id")
        storage: Optional[AccountStorage] = kwargs.get("storage")
        client_secrets_file = kwargs.get("client_secrets_file", "client_secrets.json")
        redirect_uri = kwargs.get("redirect_uri")
        if not redirect_uri:
            am_public_url = os.environ.get("B4IGO_ACCOUNT_MANAGER_PUBLIC_URL", "http://127.0.0.1:5100")
            redirect_uri = f"{am_public_url.rstrip('/')}/api/providers/gmail/oauth/callback"
        connector_name = kwargs.get("connector_name")

        if not account_id or not storage:
            raise ValueError("account_id and storage are required for Gmail setup")

        # Cleanup old sessions (older than 1 hour)
        with storage._get_connection() as conn:
            conn.execute(
                "DELETE FROM gmail_oauth_sessions"
                " WHERE created_at < datetime('now', '-1 hour')"
            )

        # Generate URL and state
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

        storage.save_gmail_oauth_session(
            state=state,
            b4igo_user_id=account_id,
            code_verifier=flow.code_verifier,
            connector_name=connector_name,
            status="pending",
        )

        return [
            EmailSetupStep(
                title="Continue to Gmail login and authorization",
                desc="You will be redirected to Google to grant read access to B4iGO.",
                type="redirect",
                value=authorization_url,
                callback=state,
                polling_id=state,
            )
        ]

    def CallFunction(
        self,
        function_name: str,
        steps: list[EmailSetupStep],
        account_id: str,
        storage: AccountStorage,
    ) -> str:
        """Validate supported callback hooks for generic setup orchestration."""
        raise ValueError(f"Unknown function name: {function_name}")

    def HandleCallback(
        self, request_args: dict[str, Any], storage: AccountStorage
    ) -> str:
        """Handle OAuth callback from Google."""
        state = request_args.get("state")
        auth_code = request_args.get("code")
        client_secrets_file = request_args.get(
            "client_secrets_file", "client_secrets.json"
        )
        redirect_uri = request_args.get("redirect_uri")
        if not redirect_uri:
            am_public_url = os.environ.get("B4IGO_ACCOUNT_MANAGER_PUBLIC_URL", "http://127.0.0.1:5100")
            redirect_uri = f"{am_public_url.rstrip('/')}/api/providers/gmail/oauth/callback"


        if not state or not auth_code:
            if state:
                storage.update_gmail_oauth_session_status(state, "error")
            return "Missing state or code in callback"

        session = storage.pop_gmail_oauth_session(state)
        if session is None:
            return "OAuth session not found or timed out"

        try:
            from google_auth_oauthlib.flow import Flow

            flow = Flow.from_client_secrets_file(
                client_secrets_file,
                scopes=["https://www.googleapis.com/auth/gmail.readonly"],
                redirect_uri=redirect_uri,
                state=state,
            )
            flow.code_verifier = session.code_verifier
            flow.fetch_token(code=auth_code)

            creds_data = flow.credentials
            credentials = {
                "token": creds_data.token,
                "refresh_token": creds_data.refresh_token,
                "token_uri": creds_data.token_uri,
                "client_id": creds_data.client_id,
                "client_secret": creds_data.client_secret,
                "scopes": creds_data.scopes,
            }

            # Resolve email address
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
            email_address = str(profile["emailAddress"])

            account = storage.upsert_account(
                b4igo_user_id=session.b4igo_user_id,
                provider="gmail",
                email_address=email_address,
                credentials=credentials,
                display_name=session.connector_name or email_address,
            )

            if account:
                storage.save_gmail_oauth_session(
                    state=state,
                    b4igo_user_id=session.b4igo_user_id,
                    code_verifier=session.code_verifier,
                    connector_name=session.connector_name,
                    status="success",
                )
                return ""
            else:
                storage.save_gmail_oauth_session(
                    state=state,
                    b4igo_user_id=session.b4igo_user_id,
                    code_verifier=session.code_verifier,
                    connector_name=session.connector_name,
                    status="error",
                )
                return "Failed to upsert Gmail account"

        except Exception as exc:
            storage.save_gmail_oauth_session(
                state=state,
                b4igo_user_id=session.b4igo_user_id,
                code_verifier=session.code_verifier,
                connector_name=session.connector_name,
                status="error",
            )
            return f"OAuth exchange failed: {exc}"
