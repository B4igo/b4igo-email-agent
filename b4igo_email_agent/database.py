"""SQLite database module for managing users and confirmations."""

import sqlite3
from contextlib import contextmanager
from typing import Optional


class Database:
    """SQLite database manager for users and confirmations."""

    def __init__(self, db_path: str = "email_agent.db"):
        """Initialize the database and create tables.

        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = db_path
        self._initialize_tables()

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
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

    def _initialize_tables(self):
        """Create users and confirmations tables."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS confirmations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    jsonPayload TEXT NOT NULL,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS email_connectors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    connector_type TEXT NOT NULL,
                    connector_name TEXT NOT NULL,
                    token_json TEXT NOT NULL,
                    connector_email TEXT NOT NULL,
                    last_read TEXT,
                    last_error_msg TEXT,
                    FOREIGN KEY (username) REFERENCES users(username),
                    UNIQUE(username, connector_email)
                )
            """
            )

    def add_user(self, username: str, password: str, role: str) -> bool:
        """Add a new user to the database.

        Args:
            username: Unique username
            password: User password
            role: User role (e.g., 'user', 'admin')

        Returns:
            True if user was added, False if username already exists.
        """
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, role),
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, username: str) -> Optional[dict]:
        """Get user by username.

        Args:
            username: Username to look up

        Returns:
            User dict with username, password, role, or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT username, password, role FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def add_confirmation(self, username: str, json_payload: str) -> Optional[int]:
        """Add a new confirmation for a user.

        Args:
            username: Username this confirmation belongs to
            json_payload: JSON payload string

        Returns:
            The generated confirmation ID, or None if user doesn't exist.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO confirmations (username, jsonPayload) VALUES (?, ?)",
                    (username, json_payload),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_confirmations(self, username: str) -> list[dict]:
        """Get all confirmations for a user.

        Args:
            username: Username to get confirmations for

        Returns:
            List of confirmation dicts with id and jsonPayload.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, jsonPayload FROM confirmations WHERE username = ?",
                (username,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def remove_confirmation(self, confirmation_id: int) -> bool:
        """Remove a confirmation by ID.

        Args:
            confirmation_id: Confirmation ID to remove

        Returns:
            True if confirmation was removed, False if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM confirmations WHERE id = ?", (confirmation_id,)
            )
            return cursor.rowcount > 0

    def confirmation_exists(self, confirmation_id: int) -> bool:
        """Check if a confirmation exists.

        Args:
            confirmation_id: Confirmation ID to check

        Returns:
            True if confirmation exists, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM confirmations WHERE id = ?", (confirmation_id,)
            )
            return cursor.fetchone() is not None

    def add_email_connector(
            self,
            username: str,
            connector_type: str,
            connector_name: str,
            token_json: str,
            connector_email: str,
            last_read: Optional[str] = None,
            last_error_msg: Optional[str] = None,
    ) -> Optional[int]:
        """Add a new email connector for a user."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO email_connectors
                       (username, connector_type, connector_name, token_json, connector_email, last_read,
                        last_error_msg)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        username,
                        connector_type,
                        connector_name,
                        token_json,
                        connector_email,
                        last_read,
                        last_error_msg,
                    ),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_email_connectors(self, username: str) -> list[dict]:
        """Get all email connectors for a user."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """SELECT id,
                          connector_type,
                          connector_name,
                          token_json,
                          connector_email,
                          last_read,
                          last_error_msg
                   FROM email_connectors
                   WHERE username = ?""",
                (username,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_email_connector(self, connector_id: int) -> Optional[dict]:
        """Get a specific email connector by ID."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """SELECT id,
                          username,
                          connector_type,
                          connector_name,
                          token_json,
                          connector_email,
                          last_read,
                          last_error_msg
                   FROM email_connectors
                   WHERE id = ?""",
                (connector_id,),
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def remove_email_connector(self, connector_id: int, username: str) -> bool:
        """Remove an email connector by ID for a specific user."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM email_connectors WHERE id = ? AND username = ?",
                (connector_id, username),
            )
            return cursor.rowcount > 0

    def update_connector_last_read(
            self, connector_id: int, last_read: str, last_error_msg: Optional[str] = None
    ) -> bool:
        """Update the last read timestamp and error message for a connector."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """UPDATE email_connectors
                   SET last_read      = ?,
                       last_error_msg = ?
                   WHERE id = ?""",
                (last_read, last_error_msg, connector_id),
            )
            return cursor.rowcount > 0

    def email_already_connected(self, username: str, connector_email: str) -> bool:
        """Check if an email address is already connected to a user's account."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """SELECT 1
                   FROM email_connectors
                   WHERE username = ?
                     AND connector_email = ?""",
                (username, connector_email),
            )
            return cursor.fetchone() is not None

# Global database instance
db = Database()