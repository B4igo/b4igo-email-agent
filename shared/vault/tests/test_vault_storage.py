"""Unit tests for VaultStorage."""

import os
import tempfile
from pathlib import Path
from unittest import TestCase

from shared.vault.storage import VaultStorage


class TestVaultStorage(TestCase):
    """Unit tests for VaultStorage CRUD."""

    def setUp(self) -> None:
        """Use a temporary DB file per test for isolation."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.storage = VaultStorage(db_path=self.tmp.name)

    def tearDown(self) -> None:
        """Remove temporary DB file."""
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_add_record_returns_id(self) -> None:
        """add_record returns new id for valid type."""
        id1 = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.assertIsNotNone(id1)
        self.assertIsInstance(id1, int)
        id2 = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. B"})
        self.assertNotEqual(id1, id2)

    def test_add_record_invalid_type_returns_none(self) -> None:
        """add_record returns None for invalid record_type."""
        self.assertIsNone(self.storage.add_record("alice", "invalid", {}))

    def test_get_records_empty(self) -> None:
        """get_records returns empty list when no records."""
        self.assertEqual(self.storage.get_records("alice"), [])
        self.assertEqual(self.storage.get_records("alice", "doctor"), [])

    def test_get_records_by_username_and_type(self) -> None:
        """get_records filters by username and optional record_type."""
        self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.storage.add_record(
            "alice",
            "insurance",
            {"type_of_health_insurance": "PPO", "coverage_type": "Family"},
        )
        self.storage.add_record("bob", "doctor", {"doctor_name": "Dr. B"})
        all_alice = self.storage.get_records("alice")
        self.assertEqual(len(all_alice), 2)
        doctors_alice = self.storage.get_records("alice", "doctor")
        self.assertEqual(len(doctors_alice), 1)
        self.assertEqual(doctors_alice[0]["payload"]["doctor_name"], "Dr. A")
        bob_recs = self.storage.get_records("bob")
        self.assertEqual(len(bob_recs), 1)
        self.assertEqual(bob_recs[0]["payload"]["doctor_name"], "Dr. B")

    def test_get_records_by_id(self) -> None:
        """get_records with id returns single record scoped by username."""
        self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. B"})
        one = self.storage.get_records("alice", id=rid)
        self.assertEqual(len(one), 1)
        self.assertEqual(one[0]["payload"]["doctor_name"], "Dr. B")
        self.assertEqual(self.storage.get_records("bob", id=rid), [])

    def test_update_record(self) -> None:
        """update_record replaces payload and returns True."""
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        assert rid is not None
        ok = self.storage.update_record(
            rid, {"doctor_name": "Dr. Updated", "type": "GP"}
        )
        self.assertTrue(ok)
        recs = self.storage.get_records("alice", id=rid)
        self.assertEqual(recs[0]["payload"]["doctor_name"], "Dr. Updated")

    def test_update_record_nonexistent_returns_false(self) -> None:
        """update_record returns False for nonexistent id."""
        self.assertFalse(self.storage.update_record(99999, {"doctor_name": "X"}))

    def test_delete_record(self) -> None:
        """delete_record removes record and returns True."""
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        assert rid is not None
        self.assertTrue(self.storage.delete_record(rid))
        self.assertEqual(self.storage.get_records("alice"), [])

    def test_delete_record_nonexistent_returns_false(self) -> None:
        """delete_record returns False for nonexistent id."""
        self.assertFalse(self.storage.delete_record(99999))


class TestVaultStorageEnvDbPath(TestCase):
    """Tests that VaultStorage reads B4IGO_VAULT_DB_PATH from the environment."""

    def setUp(self) -> None:
        """Create a temp file path and set the env var before each test."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        # Remove the file so VaultStorage creates a fresh DB at that path.
        Path(self.tmp.name).unlink(missing_ok=True)
        os.environ["B4IGO_VAULT_DB_PATH"] = self.tmp.name

    def tearDown(self) -> None:
        """Unset the env var and remove the temp DB file."""
        os.environ.pop("B4IGO_VAULT_DB_PATH", None)
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_storage_uses_env_db_path(self) -> None:
        """VaultStorage() with no args creates the DB at B4IGO_VAULT_DB_PATH."""
        storage = VaultStorage()
        self.assertEqual(storage.db_path, self.tmp.name)
        self.assertTrue(
            Path(self.tmp.name).exists(),
            "Expected DB file to be created at the env-configured path.",
        )

    def test_env_db_path_crud_works(self) -> None:
        """Basic CRUD round-trip works on the env-configured DB path."""
        storage = VaultStorage()

        rid = storage.add_record("alice", "doctor", {"doctor_name": "Dr. Env"})
        self.assertIsNotNone(rid)
        self.assertIsInstance(rid, int)

        recs = storage.get_records("alice", "doctor")
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["payload"]["doctor_name"], "Dr. Env")

        assert rid is not None
        updated = storage.update_record(rid, {"doctor_name": "Dr. Updated"})
        self.assertTrue(updated)
        recs = storage.get_records("alice", id=rid)
        self.assertEqual(recs[0]["payload"]["doctor_name"], "Dr. Updated")

        deleted = storage.delete_record(rid)
        self.assertTrue(deleted)
        self.assertEqual(storage.get_records("alice"), [])
