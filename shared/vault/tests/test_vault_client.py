"""Unit tests for VaultClient and parse_vault_record."""

import os
import tempfile
import unittest.mock
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock

from shared.schemas.health_schemas import Doctor, Insurance, MedicalHistory, Medication
from shared.vault.b4igo_api_storage import B4igoVaultApiStorage
from shared.vault.client import VaultClient, build_vault_storage_from_env
from shared.vault.storage import VaultStorage
from shared.vault.utils import parse_vault_record


class TestParseVaultRecord(TestCase):
    """Unit tests for parse_vault_record."""

    def test_doctor_payload(self) -> None:
        """Doctor payload returns Doctor instance."""
        payload = {"doctor_name": "Dr. Smith", "type": "Cardiologist"}
        record = parse_vault_record(payload)
        self.assertIsInstance(record, Doctor)
        assert record is not None
        self.assertEqual(record.doctor_name, "Dr. Smith")

    def test_insurance_payload(self) -> None:
        """Insurance payload returns Insurance instance."""
        payload = {"type_of_health_insurance": "PPO", "coverage_type": "Family"}
        record = parse_vault_record(payload)
        self.assertIsInstance(record, Insurance)
        assert record is not None
        self.assertEqual(record.coverage_type, "Family")

    def test_medication_payload(self) -> None:
        """Medication payload returns Medication instance."""
        payload = {"name_of_medicine": "Aspirin"}
        record = parse_vault_record(payload)
        self.assertIsInstance(record, Medication)
        assert record is not None
        self.assertEqual(record.name_of_medicine, "Aspirin")

    def test_medical_history_payload(self) -> None:
        """MedicalHistory payload returns MedicalHistory instance."""
        payload = {"date": "2024-01-01", "disease": "Flu"}
        record = parse_vault_record(payload)
        self.assertIsInstance(record, MedicalHistory)
        assert record is not None
        self.assertEqual(record.disease, "Flu")

    def test_invalid_payload_returns_none(self) -> None:
        """Unknown or invalid payload returns None."""
        self.assertIsNone(parse_vault_record({}))
        self.assertIsNone(parse_vault_record({"foo": "bar"}))
        self.assertIsNone(parse_vault_record(None))


class TestVaultClient(TestCase):
    """Unit tests for VaultClient CRUD."""

    def setUp(self) -> None:
        """Use temporary DB and VaultStorage for isolation."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        storage = VaultStorage(db_path=self.tmp.name)
        self.client = VaultClient(storage=storage)

    def tearDown(self) -> None:
        """Remove temporary DB file."""
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_create_doctor_returns_id(self) -> None:
        """create with Doctor returns new id."""
        record = Doctor(doctor_name="Dr. A", type="GP")
        rid = self.client.create("alice", record)
        self.assertIsNotNone(rid)
        recs = self.client.read("alice", record_type="doctor")
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["payload"]["doctor_name"], "Dr. A")

    def test_create_insurance_medication_medical_history(self) -> None:
        """create works for Insurance, Medication, MedicalHistory."""
        self.assertIsNotNone(
            self.client.create(
                "alice",
                Insurance(type_of_health_insurance="HMO", coverage_type="Individual"),
            )
        )
        self.assertIsNotNone(
            self.client.create("alice", Medication(name_of_medicine="Ibuprofen"))
        )
        self.assertIsNotNone(
            self.client.create(
                "alice", MedicalHistory(date="2024-01-01", disease="Cold")
            )
        )
        self.assertEqual(len(self.client.read("alice")), 3)

    def test_read_filter_by_type(self) -> None:
        """read with record_type filters results."""
        self.client.create("alice", Doctor(doctor_name="Dr. X"))
        self.client.create(
            "alice", Insurance(type_of_health_insurance="PPO", coverage_type="Family")
        )
        doctors = self.client.read("alice", record_type="doctor")
        self.assertEqual(len(doctors), 1)
        self.assertEqual(doctors[0]["record_type"], "doctor")

    def test_update(self) -> None:
        """update modifies existing record."""
        rid = self.client.create("alice", Doctor(doctor_name="Dr. Old"))
        assert rid is not None
        self.assertTrue(self.client.update(rid, Doctor(doctor_name="Dr. New")))
        recs = self.client.read("alice", id=rid)
        self.assertEqual(recs[0]["payload"]["doctor_name"], "Dr. New")

    def test_delete(self) -> None:
        """delete removes record."""
        rid = self.client.create("alice", Doctor(doctor_name="Dr. X"))
        assert rid is not None
        self.assertTrue(self.client.delete(rid))
        self.assertEqual(self.client.read("alice"), [])


class TestBuildVaultStorageFromEnv(TestCase):
    """Tests for build_vault_storage_from_env backend selection."""

    def tearDown(self) -> None:
        """Clean up env vars after each test."""
        os.environ.pop("B4IGO_VAULT_BACKEND", None)
        os.environ.pop("B4IGO_API_BASE_URL", None)

    def test_default_returns_vault_storage(self) -> None:
        """Returns VaultStorage when no B4IGO_VAULT_BACKEND env var is set."""
        os.environ.pop("B4IGO_VAULT_BACKEND", None)
        os.environ.pop("B4IGO_API_BASE_URL", None)
        storage = build_vault_storage_from_env()
        self.assertIsInstance(storage, VaultStorage)

    def test_api_backend_returns_b4igo_api_storage(self) -> None:
        """Returns B4igoVaultApiStorage when backend=api and base URL is set."""
        os.environ["B4IGO_VAULT_BACKEND"] = "api"
        os.environ["B4IGO_API_BASE_URL"] = "https://example.com"
        mock_session = MagicMock()
        patch_target = "shared.vault.client.B4igoVaultApiStorage"
        with unittest.mock.patch(patch_target) as mock_cls:
            mock_cls.return_value = B4igoVaultApiStorage(
                base_url="https://example.com", session=mock_session
            )
            storage = build_vault_storage_from_env()
            mock_cls.assert_called_once_with(base_url="https://example.com")
        self.assertIsInstance(storage, B4igoVaultApiStorage)

    def test_api_backend_without_url_falls_back_to_vault_storage(self) -> None:
        """Returns VaultStorage when B4IGO_VAULT_BACKEND=api but no URL is set."""
        os.environ["B4IGO_VAULT_BACKEND"] = "api"
        os.environ.pop("B4IGO_API_BASE_URL", None)
        storage = build_vault_storage_from_env()
        self.assertIsInstance(storage, VaultStorage)
