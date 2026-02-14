"""Unit tests for VaultClient and parse_vault_record."""

import tempfile
from pathlib import Path
from unittest import TestCase

from b4igo_email_agent.ai_pipeline.schemas.schemas import (
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)
from b4igo_email_agent.vault.client import VaultClient
from b4igo_email_agent.vault.storage import VaultStorage
from b4igo_email_agent.vault.utils import parse_vault_record


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
