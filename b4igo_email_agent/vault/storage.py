"""SQLite storage for vault records (doctors, insurance, meds, medical_history)."""

import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Optional

VAULT_RECORD_TYPES = ("doctor", "insurance", "medication", "medical_history")


class VaultStorage:
    """SQLite storage for vault CRUD. One table keyed by username and record_type."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize vault storage.

        Args:
            db_path: Path to SQLite database. Defaults to B4IGO_VAULT_DB_PATH env
                or email_agent.db in cwd for simplicity.
        """
        self.db_path = db_path or os.environ.get(
            "B4IGO_VAULT_DB_PATH", "email_agent.db"
        )
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

    def _initialize_tables(self) -> None:
        """Create vault_records table if not exists."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS vault_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    CHECK (record_type IN (
                        'doctor', 'insurance', 'medication', 'medical_history'
                    ))
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_vault_username "
                "ON vault_records(username)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_vault_username_type "
                "ON vault_records(username, record_type)"
            )

    def add_record(
        self, username: str, record_type: str, payload: dict[str, Any]
    ) -> Optional[int]:
        """Add a vault record.

        Args:
            username: Owner of the record.
            record_type: One of doctor, insurance, medication, medical_history.
            payload: JSON-serializable dict (schema fields).

        Returns:
            The new record id, or None on error.
        """
        if record_type not in VAULT_RECORD_TYPES:
            return None
        try:
            payload_str = json.dumps(payload)
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO vault_records "
                    "(username, record_type, payload) VALUES (?, ?, ?)",
                    (username, record_type, payload_str),
                )
                return cursor.lastrowid
        except (TypeError, sqlite3.IntegrityError):
            return None

    def get_records(
        self,
        username: str,
        record_type: Optional[str] = None,
        id: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Get vault records for a user, optionally by type or single id.

        Args:
            username: Owner to filter by.
            record_type: Optional filter (doctor, insurance, medication,
                medical_history).
            id: Optional single record id (still scoped by username if provided).

        Returns:
            List of dicts with id, username, record_type, payload (parsed JSON).
        """
        with self._get_connection() as conn:
            if id is not None:
                cursor = conn.execute(
                    "SELECT id, username, record_type, payload FROM vault_records "
                    "WHERE id = ? AND username = ?",
                    (id, username),
                )
            elif record_type and record_type in VAULT_RECORD_TYPES:
                cursor = conn.execute(
                    "SELECT id, username, record_type, payload FROM vault_records "
                    "WHERE username = ? AND record_type = ?",
                    (username, record_type),
                )
            else:
                cursor = conn.execute(
                    "SELECT id, username, record_type, payload FROM vault_records "
                    "WHERE username = ?",
                    (username,),
                )
            rows = cursor.fetchall()
        out = []
        for row in rows:
            r = dict(row)
            try:
                r["payload"] = json.loads(r["payload"])
            except (TypeError, json.JSONDecodeError):
                r["payload"] = {}
            out.append(r)
        return out

    def update_record(self, id: int, payload: dict[str, Any]) -> bool:
        """Update a vault record by id.

        Args:
            id: Record id.
            payload: New JSON-serializable dict.

        Returns:
            True if a row was updated, False otherwise.
        """
        try:
            payload_str = json.dumps(payload)
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "UPDATE vault_records SET payload = ? WHERE id = ?",
                    (payload_str, id),
                )
                return cursor.rowcount > 0
        except TypeError:
            return False

    def delete_record(self, id: int) -> bool:
        """Delete a vault record by id.

        Args:
            id: Record id.

        Returns:
            True if a row was deleted, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM vault_records WHERE id = ?", (id,))
            return cursor.rowcount > 0
