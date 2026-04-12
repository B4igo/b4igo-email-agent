"""SQLite storage for AccountManager linked email accounts."""

import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Optional

from .models import GmailOAuthSession, LinkedAccount, ProviderType


class AccountStorage:
    """SQLite storage layer for linked email provider accounts."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the account storage.

        Args:
            db_path: Path to sqlite db file. Defaults to
                B4IGO_ACCOUNT_DB_PATH or email_agent.db.
        """
        self.db_path = db_path or os.environ.get(
            "B4IGO_ACCOUNT_DB_PATH", "email_agent.db"
        )
        self._initialize_tables()

    @contextmanager
    def _get_connection(self):
        """Context manager for sqlite connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _initialize_tables(self) -> None:
        """Create account manager tables if they do not exist."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS linked_email_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    b4igo_user_id TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    email_address TEXT NOT NULL,
                    display_name TEXT,
                    credentials_json TEXT NOT NULL,
                    config_json TEXT NOT NULL,
                    last_read TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (b4igo_user_id, provider, email_address)
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_accounts_user "
                "ON linked_email_accounts(b4igo_user_id)"
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS gmail_oauth_sessions (
                    state TEXT PRIMARY KEY,
                    b4igo_user_id TEXT NOT NULL,
                    code_verifier TEXT NOT NULL,
                    connector_name TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def upsert_user(self, username: str, password: str, role: str) -> dict[str, Any]:
        """Create or update one user credential record."""
        with self._get_connection() as conn:
            existing = conn.execute(
                "SELECT username FROM users WHERE username = ?",
                (username,),
            ).fetchone()
            if existing is None:
                conn.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, role),
                )
            else:
                conn.execute(
                    """
                    UPDATE users
                    SET password = ?, role = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE username = ?
                    """,
                    (password, role, username),
                )

            row = conn.execute(
                "SELECT username, role, created_at, updated_at FROM users WHERE username = ?",
                (username,),
            ).fetchone()

        return {
            "username": row["username"],
            "role": row["role"],
            "createdAt": row["created_at"],
            "updatedAt": row["updated_at"],
        }

    def get_user(self, username: str) -> Optional[dict[str, Any]]:
        """Return one user record including password for auth checks."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT username, password, role FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        if row is None:
            return None
        return {
            "username": row["username"],
            "password": row["password"],
            "role": row["role"],
        }

    def user_exists(self, username: str) -> bool:
        """Return whether the given username exists."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT 1 FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        return row is not None

    def save_gmail_oauth_session(
        self,
        state: str,
        b4igo_user_id: str,
        code_verifier: str,
        connector_name: Optional[str] = None,
    ) -> None:
        """Persist Gmail OAuth state and PKCE verifier for callback completion."""
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO gmail_oauth_sessions
                (state, b4igo_user_id, code_verifier, connector_name)
                VALUES (?, ?, ?, ?)
                """,
                (state, b4igo_user_id, code_verifier, connector_name),
            )

    def pop_gmail_oauth_session(self, state: str) -> Optional[GmailOAuthSession]:
        """Load and delete one Gmail OAuth session by state."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM gmail_oauth_sessions WHERE state = ?",
                (state,),
            ).fetchone()
            if row is None:
                return None
            conn.execute("DELETE FROM gmail_oauth_sessions WHERE state = ?", (state,))

        return GmailOAuthSession(
            state=row["state"],
            b4igo_user_id=row["b4igo_user_id"],
            code_verifier=row["code_verifier"],
            connector_name=row["connector_name"],
            created_at=row["created_at"],
        )

    def upsert_account(
        self,
        b4igo_user_id: str,
        provider: ProviderType,
        email_address: str,
        credentials: dict[str, Any],
        display_name: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
    ) -> Optional[LinkedAccount]:
        """Insert or update a linked account for a user.

        Args:
            b4igo_user_id: B4iGO user identifier.
            provider: Linked provider type.
            email_address: Email address on provider.
            credentials: Provider credentials payload.
            display_name: Optional account label.
            config: Optional provider settings.

        Returns:
            Persisted linked account, or None if payload cannot be serialized.
        """
        config_payload = config or {}
        try:
            credentials_json = json.dumps(credentials)
            config_json = json.dumps(config_payload)
        except TypeError:
            return None

        with self._get_connection() as conn:
            existing = conn.execute(
                "SELECT id FROM linked_email_accounts "
                "WHERE b4igo_user_id = ? AND provider = ? AND email_address = ?",
                (b4igo_user_id, provider, email_address),
            ).fetchone()

            if existing is None:
                cursor = conn.execute(
                    """
                    INSERT INTO linked_email_accounts
                    (b4igo_user_id, provider, email_address, display_name,
                     credentials_json, config_json)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        b4igo_user_id,
                        provider,
                        email_address,
                        display_name,
                        credentials_json,
                        config_json,
                    ),
                )
                account_id = cursor.lastrowid
            else:
                account_id = existing["id"]
                conn.execute(
                    """
                    UPDATE linked_email_accounts
                    SET display_name = ?, credentials_json = ?, config_json = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (display_name, credentials_json, config_json, account_id),
                )

            row = conn.execute(
                "SELECT * FROM linked_email_accounts WHERE id = ?", (account_id,)
            ).fetchone()
            if row is None:
                return None
            return _row_to_linked_account(row)

    def list_accounts(self, b4igo_user_id: str) -> list[LinkedAccount]:
        """Return all linked accounts for a user."""
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM linked_email_accounts WHERE b4igo_user_id = ? "
                "ORDER BY id ASC",
                (b4igo_user_id,),
            ).fetchall()
        return [_row_to_linked_account(row) for row in rows]

    def get_account(
        self, b4igo_user_id: str, account_id: int
    ) -> Optional[LinkedAccount]:
        """Return one linked account by id and user."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM linked_email_accounts "
                "WHERE id = ? AND b4igo_user_id = ?",
                (account_id, b4igo_user_id),
            ).fetchone()
        return _row_to_linked_account(row) if row else None

    def get_accounts_by_ids(
        self,
        b4igo_user_id: str,
        account_ids: list[int],
    ) -> list[LinkedAccount]:
        """Return linked accounts filtered by id list for one user."""
        if not account_ids:
            return self.list_accounts(b4igo_user_id)

        placeholders = ",".join("?" for _ in account_ids)
        params: list[Any] = [b4igo_user_id] + account_ids
        query = (
            "SELECT * FROM linked_email_accounts "
            f"WHERE b4igo_user_id = ? AND id IN ({placeholders}) "
            "ORDER BY id ASC"
        )
        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
        return [_row_to_linked_account(row) for row in rows]

    def delete_account(self, b4igo_user_id: str, account_id: int) -> bool:
        """Delete one linked account."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM linked_email_accounts "
                "WHERE id = ? AND b4igo_user_id = ?",
                (account_id, b4igo_user_id),
            )
            return cursor.rowcount > 0

    def update_last_read(self, account_id: int, last_read: datetime) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                UPDATE linked_email_accounts
                SET last_read = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (last_read.astimezone(timezone.utc).isoformat(), account_id),
            )

def _row_to_linked_account(row: sqlite3.Row) -> LinkedAccount:
    """Convert sqlite row into LinkedAccount."""
    credentials: dict[str, Any]
    config: dict[str, Any]
    try:
        credentials = (
            json.loads(row["credentials_json"]) if row["credentials_json"] else {}
        )
    except json.JSONDecodeError:
        credentials = {}
    try:
        config = json.loads(row["config_json"]) if row["config_json"] else {}
    except json.JSONDecodeError:
        config = {}

    return LinkedAccount(
        id=row["id"],
        b4igo_user_id=row["b4igo_user_id"],
        provider=row["provider"],
        email_address=row["email_address"],
        display_name=row["display_name"],
        credentials=credentials,
        config=config,
        last_read=row["last_read"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )
