"""SQLite storage for vault records (doctor, insurance, medication, history)."""

import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Optional

VAULT_RECORD_TYPES = (
    # health
    "doctor",
    "insurance",
    "medication",
    "medical_history",
    # education
    "education",
    # legal
    "attorney",
    "contract",
    "court_date",
    "legal_notice",
    # personal
    "contact",
    "personal_event",
    "reminder",
)


class VaultStorage:
    """SQLite storage for vault CRUD with simple JSON payloads."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize vault storage.

        Args:
            db_path: SQLite file path. Defaults to B4IGO_VAULT_DB_PATH
                or email_agent.db in cwd.
        """
        self.db_path = db_path or os.environ.get(
            "B4IGO_VAULT_DB_PATH", "email_agent.db"
        )
        self._initialize_tables()

    @contextmanager
    def _get_connection(self):
        """Yield a short-lived SQLite connection."""
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
        """Create table and indexes if they do not exist."""
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
        """Persist a new vault record and return its id."""
        if record_type not in VAULT_RECORD_TYPES:
            return None
        try:
            payload_str = json.dumps(payload)
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO vault_records (username, record_type, payload) "
                    "VALUES (?, ?, ?)",
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
        """Read records by username and optional filters."""
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

        out: list[dict[str, Any]] = []
        for row in rows:
            record = dict(row)
            try:
                record["payload"] = json.loads(record["payload"])
            except (TypeError, json.JSONDecodeError):
                record["payload"] = {}
            out.append(record)
        return out

    def update_record(
        self,
        id: int,
        payload: dict[str, Any],
        record_type: str = "",
        username: str = "",
    ) -> bool:
        """Replace payload for an existing record id."""
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

    def delete_record(self, id: int, record_type: str = "", username: str = "") -> bool:
        """Delete a record by id."""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM vault_records WHERE id = ?", (id,))
            return cursor.rowcount > 0
