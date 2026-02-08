"""SQLite database module for managing users and confirmations."""

import sqlite3
from contextlib import contextmanager
from typing import Optional


class Database:
    """SQLite database manager for users and confirmations."""

    def __init__(self, db_path: str = ":memory:"):
        """Initialize the database and create tables.

        Args:
            db_path: Path to SQLite database file. Use ':memory:' for in-memory DB.
        """
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._initialize_tables()

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        try:
            yield self._conn
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise

    def _initialize_tables(self):
        """Create users and confirmations tables."""
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS confirmations (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                jsonPayload TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """
        )
        self._conn.commit()

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

    def add_confirmation(
        self, confirmation_id: int, username: str, json_payload: str
    ) -> bool:
        """Add a new confirmation for a user.

        Args:
            confirmation_id: Unique confirmation ID
            username: Username this confirmation belongs to
            json_payload: JSON payload string

        Returns:
            True if confirmation was added, False if ID already exists.
        """
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO confirmations (id, username, jsonPayload) "
                    "VALUES (?, ?, ?)",
                    (confirmation_id, username, json_payload),
                )
            return True
        except sqlite3.IntegrityError:
            return False

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


# Global database instance (using shared in-memory database for testing)
db = Database("file::memory:?mode=memory&cache=shared")
