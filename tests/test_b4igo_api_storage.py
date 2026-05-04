"""Unit tests for B4igoVaultApiStorage."""

from unittest import TestCase, mock

from shared.vault.b4igo_api_storage import B4igoVaultApiStorage


def _gql_ok(name: str, extra: dict) -> mock.MagicMock:
    resp = mock.MagicMock()
    resp.json.return_value = {"data": {name: {"success": True, **extra}}}
    return resp


def _gql_error() -> mock.MagicMock:
    resp = mock.MagicMock()
    resp.json.return_value = {"errors": [{"message": "server error"}]}
    return resp


class TestB4igoVaultApiStorage(TestCase):
    """Tests for the GraphQL-backed storage adapter."""

    def setUp(self) -> None:
        self.session = mock.MagicMock()
        self.storage = B4igoVaultApiStorage(
            base_url="https://api.example.com",
            api_key="token",
            timeout_seconds=2,
            session=self.session,
        )

    def _variables(self) -> dict:
        return self.session.post.call_args.kwargs["json"]["variables"]

    # --- add_record ---

    def test_add_record_doctor_returns_id(self) -> None:
        self.session.post.return_value = _gql_ok(
            "createFamilyDoctor", {"data": {"doctorId": 42}}
        )
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.assertEqual(rid, 42)

    def test_add_record_medication_uses_id(self) -> None:
        self.session.post.return_value = _gql_ok("createMedicationAndAllergy", {"id": 7})
        rid = self.storage.add_record(
            "alice", "medication", {"name_of_medicine": "Aspirin"}
        )
        self.assertEqual(rid, 7)

    def test_add_record_returns_none_on_graphql_error(self) -> None:
        self.session.post.return_value = _gql_error()
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.assertIsNone(rid)

    def test_add_record_doctor_sends_correct_fields(self) -> None:
        self.session.post.return_value = _gql_ok(
            "createFamilyDoctor", {"data": {"doctorId": 1}}
        )
        self.storage.add_record(
            "alice", "doctor", {"doctor_name": "Dr. Smith"}
        )
        inp = self._variables()["input"]
        self.assertEqual(inp["userId"], "alice")
        self.assertEqual(inp["doctorName"], "Dr. Smith")
        self.assertIn("typeId", inp)

    def test_add_record_medication_sends_correct_fields(self) -> None:
        self.session.post.return_value = _gql_ok("createMedicationAndAllergy", {"id": 2})
        self.storage.add_record(
            "alice",
            "medication",
            {"name_of_medicine": "Ibuprofen", "side_effect": "Nausea"},
        )
        inp = self._variables()["input"]
        self.assertEqual(inp["userId"], "alice")
        self.assertEqual(inp["medicineName"], "Ibuprofen")
        self.assertEqual(inp["sideEffect"], "Nausea")

    def test_add_record_insurance_sends_correct_fields(self) -> None:
        self.session.post.return_value = _gql_ok("createHealthInsurance", {"id": 3})
        self.storage.add_record(
            "alice",
            "insurance",
            {"type_of_health_insurance": "PPO"},
        )
        inp = self._variables()["input"]
        self.assertEqual(inp["userId"], "alice")
        self.assertEqual(inp["memberName"], "PPO")
        self.assertIn("insuranceTypeId", inp)

    def test_add_record_medical_history_sends_correct_fields(self) -> None:
        self.session.post.return_value = _gql_ok("createMedicalHistories", {"id": 4})
        self.storage.add_record(
            "alice",
            "medical_history",
            {"disease": "Hypertension"},
        )
        inp = self._variables()["input"]
        self.assertEqual(inp["userId"], "alice")
        self.assertEqual(inp["generalHealth"], "Hypertension")

    def test_add_record_medical_history_appends_description(self) -> None:
        self.session.post.return_value = _gql_ok("createMedicalHistories", {"id": 5})
        self.storage.add_record(
            "alice",
            "medical_history",
            {"disease": "Diabetes", "description": "Type 2"},
        )
        inp = self._variables()["input"]
        self.assertEqual(inp["generalHealth"], "Diabetes - Type 2")

    # --- get_records ---

    def test_get_records_normalizes_doctor_list(self) -> None:
        resp = mock.MagicMock()
        resp.json.return_value = {
            "data": {
                "getAllDoctors": {
                    "success": True,
                    "doctor": [
                        {"doctorId": 1, "userId": "alice", "doctorName": "Dr. A"}
                    ],
                }
            }
        }
        self.session.post.return_value = resp
        records = self.storage.get_records("alice", record_type="doctor")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["payload"]["doctor_name"], "Dr. A")

    def test_get_records_normalizes_medication_list(self) -> None:
        resp = mock.MagicMock()
        resp.json.return_value = {
            "data": {
                "getMedicationsByUserId": {
                    "success": True,
                    "data": [
                        {"medicationId": 2, "userId": "alice", "medicineName": "Aspirin"}
                    ],
                }
            }
        }
        self.session.post.return_value = resp
        records = self.storage.get_records("alice", record_type="medication")
        self.assertEqual(len(records), 1)

    def test_get_records_sends_userId_variable(self) -> None:
        resp = mock.MagicMock()
        resp.json.return_value = {
            "data": {"getAllDoctors": {"success": True, "doctor": []}}
        }
        self.session.post.return_value = resp
        self.storage.get_records("alice", record_type="doctor")
        self.assertEqual(self._variables()["userId"], "alice")

    # --- update_record ---

    def test_update_record_doctor_sends_doctorId(self) -> None:
        self.session.post.return_value = _gql_ok("updateFamilyDoctor", {})
        ok = self.storage.update_record(
            10, {"doctor_name": "Dr. New"}, record_type="doctor", username="alice"
        )
        self.assertTrue(ok)
        inp = self._variables()["input"]
        self.assertEqual(inp["doctorId"], 10)
        self.assertEqual(inp["userId"], "alice")
        self.assertEqual(inp["doctorName"], "Dr. New")

    def test_update_record_medication_sends_recordId(self) -> None:
        self.session.post.return_value = _gql_ok("updateMedicationAndAllergies", {})
        self.storage.update_record(
            5,
            {"name_of_medicine": "Tylenol"},
            record_type="medication",
            username="alice",
        )
        inp = self._variables()["input"]
        self.assertEqual(inp["recordId"], 5)
        self.assertEqual(inp["medication"], "Tylenol")

    def test_update_record_insurance_sends_insuranceId(self) -> None:
        self.session.post.return_value = _gql_ok("updateHealthInsurance", {})
        self.storage.update_record(
            3,
            {"type_of_health_insurance": "HMO"},
            record_type="insurance",
            username="alice",
        )
        inp = self._variables()["input"]
        self.assertEqual(inp["insuranceId"], 3)
        self.assertEqual(inp["insuranceName"], "HMO")

    def test_update_record_medical_history_sends_historyId(self) -> None:
        self.session.post.return_value = _gql_ok("updateMedicalHistory", {})
        self.storage.update_record(
            8,
            {"disease": "Asthma"},
            record_type="medical_history",
            username="alice",
        )
        inp = self._variables()["input"]
        self.assertEqual(inp["historyId"], 8)
        self.assertEqual(inp["history"], "Asthma")

    def test_update_record_returns_false_on_error(self) -> None:
        self.session.post.return_value = _gql_error()
        ok = self.storage.update_record(
            10, {"doctor_name": "Dr. New"}, record_type="doctor", username="alice"
        )
        self.assertFalse(ok)

    # --- delete_record ---

    def test_delete_record_doctor_sends_id(self) -> None:
        self.session.post.return_value = _gql_ok("deleteDoctorDetails", {})
        self.storage.delete_record(10, record_type="doctor", username="alice")
        inp = self._variables()["input"]
        self.assertEqual(inp["id"], 10)
        self.assertEqual(inp["userId"], "alice")

    def test_delete_record_medication_sends_id(self) -> None:
        self.session.post.return_value = _gql_ok("deleteMedicationAllergies", {})
        self.storage.delete_record(5, record_type="medication", username="alice")
        self.assertEqual(self._variables()["input"]["id"], 5)

    def test_delete_record_insurance_sends_id(self) -> None:
        self.session.post.return_value = _gql_ok("deleteHealthInsurance", {})
        self.storage.delete_record(3, record_type="insurance", username="alice")
        self.assertEqual(self._variables()["input"]["id"], 3)

    def test_delete_record_medical_history_sends_id(self) -> None:
        self.session.post.return_value = _gql_ok("deleteMedicalHistory", {})
        self.storage.delete_record(8, record_type="medical_history", username="alice")
        self.assertEqual(self._variables()["input"]["id"], 8)

    def test_delete_record_returns_false_on_failure(self) -> None:
        self.session.post.return_value = _gql_error()
        ok = self.storage.delete_record(10, record_type="doctor", username="alice")
        self.assertFalse(ok)

    # --- correlation ID ---

    def test_request_includes_correlation_id(self) -> None:
        resp = mock.MagicMock()
        resp.json.return_value = {
            "data": {"getAllDoctors": {"success": True, "doctor": []}}
        }
        self.session.post.return_value = resp
        self.storage.get_records("alice", record_type="doctor")
        headers = self.session.post.call_args.kwargs["headers"]
        self.assertIn("X-Correlation-ID", headers)
