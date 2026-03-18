"""Unit tests for B4igoVaultApiStorage."""

from unittest import TestCase, mock

from b4igo_email_agent.vault.b4igo_api_storage import B4igoVaultApiStorage


def _response(status_code: int, payload):
    resp = mock.MagicMock()
    resp.status_code = status_code
    resp.json.return_value = payload
    return resp


class TestB4igoVaultApiStorage(TestCase):
    """Tests for the HTTP-backed storage adapter."""

    def setUp(self) -> None:
        self.session = mock.MagicMock()
        self.storage = B4igoVaultApiStorage(
            base_url="https://api.example.com",
            api_key="token",
            timeout_seconds=2,
            session=self.session,
        )

    # --- add_record ---

    def test_add_record_doctor_returns_id(self) -> None:
        self.session.request.return_value = _response(201, {"id": 42})
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.assertEqual(rid, 42)

    def test_add_record_medication_uses_medicationId(self) -> None:
        self.session.request.return_value = _response(201, {"medicationId": 7})
        rid = self.storage.add_record(
            "alice", "medication", {"name_of_medicine": "Aspirin"}
        )
        self.assertEqual(rid, 7)

    def test_add_record_non_2xx_returns_none(self) -> None:
        self.session.request.return_value = _response(500, {"error": "x"})
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.assertIsNone(rid)

    def test_add_record_doctor_sends_correct_fields(self) -> None:
        self.session.request.return_value = _response(201, {"id": 1})
        self.storage.add_record(
            "alice", "doctor", {"doctor_name": "Dr. Smith", "type": "Cardiologist"}
        )
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["userId"], "alice")
        self.assertEqual(body["doctorName"], "Dr. Smith")
        self.assertEqual(body["typeName"], "Cardiologist")
        self.assertIn("typeId", body)

    def test_add_record_medication_sends_correct_fields(self) -> None:
        self.session.request.return_value = _response(201, {"medicationId": 2})
        self.storage.add_record(
            "alice",
            "medication",
            {
                "name_of_medicine": "Ibuprofen",
                "purpose": "Pain relief",
                "date": "2024-01-01",
            },
        )
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["userId"], "alice")
        self.assertEqual(body["medicine_name"], "Ibuprofen")
        self.assertEqual(body["purpose"], "Pain relief")
        self.assertEqual(body["start_date"], "2024-01-01")

    def test_add_record_insurance_sends_correct_fields(self) -> None:
        self.session.request.return_value = _response(201, {"id": 3})
        self.storage.add_record(
            "alice",
            "insurance",
            {"type_of_health_insurance": "PPO", "coverage_type": "Individual"},
        )
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["userId"], "alice")
        self.assertEqual(body["othersValue"], "PPO")
        self.assertIn("InsuranceTypeId", body)

    def test_add_record_medical_history_sends_correct_fields(self) -> None:
        self.session.request.return_value = _response(201, {"id": 4})
        self.storage.add_record(
            "alice",
            "medical_history",
            {"disease": "Hypertension", "date": "2023-06-01"},
        )
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["userId"], "alice")
        self.assertEqual(body["history"], "Hypertension")
        self.assertEqual(body["recordDate"], "2023-06-01")

    def test_add_record_medical_history_appends_description(self) -> None:
        self.session.request.return_value = _response(201, {"id": 5})
        self.storage.add_record(
            "alice",
            "medical_history",
            {"disease": "Diabetes", "description": "Type 2", "date": "2022-01-01"},
        )
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["history"], "Diabetes - Type 2")

    # --- get_records ---

    def test_get_records_normalizes_records_list(self) -> None:
        self.session.request.return_value = _response(
            200,
            {
                "records": [
                    {
                        "id": 1,
                        "username": "alice",
                        "record_type": "doctor",
                        "payload": {"doctor_name": "Dr. A"},
                    }
                ]
            },
        )
        records = self.storage.get_records("alice", record_type="doctor")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["payload"]["doctor_name"], "Dr. A")

    def test_get_records_normalizes_data_list(self) -> None:
        self.session.request.return_value = _response(
            200,
            {"data": [{"id": 2, "record_type": "medication", "payload": {}}]},
        )
        records = self.storage.get_records("alice", record_type="medication")
        self.assertEqual(len(records), 1)

    def test_get_records_uses_userId_param(self) -> None:
        self.session.request.return_value = _response(200, {"records": []})
        self.storage.get_records("alice")
        _, kwargs = self.session.request.call_args
        self.assertEqual(kwargs["params"]["userId"], "alice")

    # --- update_record ---

    def test_update_record_doctor_sends_doctorId(self) -> None:
        self.session.request.return_value = _response(200, {"ok": True})
        ok = self.storage.update_record(
            10, {"doctor_name": "Dr. New"}, record_type="doctor", username="alice"
        )
        self.assertTrue(ok)
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["doctorId"], 10)
        self.assertEqual(body["userId"], "alice")
        self.assertEqual(body["doctorName"], "Dr. New")

    def test_update_record_medication_sends_recordId(self) -> None:
        self.session.request.return_value = _response(200, {"ok": True})
        self.storage.update_record(
            5,
            {"name_of_medicine": "Tylenol"},
            record_type="medication",
            username="alice",
        )
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["recordId"], 5)
        self.assertEqual(body["medication"], "Tylenol")

    def test_update_record_insurance_sends_insuranceId(self) -> None:
        self.session.request.return_value = _response(200, {"ok": True})
        self.storage.update_record(
            3,
            {"type_of_health_insurance": "HMO"},
            record_type="insurance",
            username="alice",
        )
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["insuranceId"], 3)
        self.assertEqual(body["insuranceName"], "HMO")

    def test_update_record_medical_history_sends_historyId(self) -> None:
        self.session.request.return_value = _response(200, {"ok": True})
        self.storage.update_record(
            8,
            {"disease": "Asthma"},
            record_type="medical_history",
            username="alice",
        )
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["historyId"], 8)
        self.assertEqual(body["history"], "Asthma")

    def test_update_record_returns_false_on_error(self) -> None:
        self.session.request.return_value = _response(404, {})
        ok = self.storage.update_record(10, {"doctor_name": "Dr. New"})
        self.assertFalse(ok)

    # --- delete_record ---

    def test_delete_record_doctor_sends_doctorId(self) -> None:
        self.session.request.return_value = _response(200, {})
        self.storage.delete_record(10, record_type="doctor", username="alice")
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["doctorId"], 10)
        self.assertEqual(body["userId"], "alice")

    def test_delete_record_medication_sends_recordId(self) -> None:
        self.session.request.return_value = _response(200, {})
        self.storage.delete_record(5, record_type="medication", username="alice")
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["recordId"], 5)

    def test_delete_record_insurance_sends_insuranceId(self) -> None:
        self.session.request.return_value = _response(200, {})
        self.storage.delete_record(3, record_type="insurance", username="alice")
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["insuranceId"], 3)

    def test_delete_record_medical_history_sends_historyId(self) -> None:
        self.session.request.return_value = _response(200, {})
        self.storage.delete_record(8, record_type="medical_history", username="alice")
        _, kwargs = self.session.request.call_args
        body = kwargs["json"]
        self.assertEqual(body["historyId"], 8)

    def test_delete_record_returns_false_on_failure(self) -> None:
        self.session.request.return_value = _response(404, {"ok": False})
        ok = self.storage.delete_record(10)
        self.assertFalse(ok)

    # --- correlation ID ---

    def test_request_includes_correlation_id(self) -> None:
        self.session.request.return_value = _response(200, {"records": []})
        _ = self.storage.get_records("alice")
        kwargs = self.session.request.call_args.kwargs
        self.assertIn("headers", kwargs)
        self.assertIn("X-Correlation-ID", kwargs["headers"])
