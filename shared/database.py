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
        """Create the confirmations table."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS confirmations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    json_payload TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """
            )

    def add_confirmation(self, user_id: str, json_payload: str) -> Optional[int]:
        """Add a new confirmation for a user.

        Args:
            user_id: User ID this confirmation belongs to
            json_payload: JSON payload string

        Returns:
            The generated confirmation ID, or None if user doesn't exist.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO confirmations (user_id, json_payload) VALUES (?, ?)",
                    (user_id, json_payload),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_confirmations(self, user_id: str) -> list[dict]:
        """Get all confirmations for a user.

        Args:
            user_id: User ID to get confirmations for

        Returns:
            List of confirmation dicts with id and jsonPayload.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, json_payload FROM confirmations WHERE user_id = ?",
                (user_id,),
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

    def clear_confirmations(self, username: Optional[str] = None) -> int:
        """Delete all confirmations, optionally scoped to a single user.

        Args:
            username: If provided, only that user's confirmations are removed.

        Returns:
            Number of rows deleted.
        """
        with self._get_connection() as conn:
            if username is None:
                cursor = conn.execute("DELETE FROM confirmations")
            else:
                cursor = conn.execute(
                    "DELETE FROM confirmations WHERE username = ?", (username,)
                )
            return cursor.rowcount


# Global database instance
db = Database()
