"""Unit tests for B4igoVaultApiStorage."""

from unittest import TestCase, mock

from shared.vault.b4igo_api_storage import B4igoVaultApiStorage


def _graphql_response(
    mutation_name, success=True, id_value=None, errors=None, nested_id_field=None
):
    """Build a mock GraphQL response.

    Args:
        mutation_name: Name of the mutation or query.
        success: Whether the mutation/query succeeded.
        id_value: ID value to return in the create mutation response.
        errors: Optional list of error dicts.
        nested_id_field: If set, id_value is nested inside data[field];
            otherwise id_value is placed flat on the mutation result.

    Returns:
        Mock response object with .json() method.
    """
    resp = mock.MagicMock()
    if errors:
        resp.json.return_value = {"errors": errors}
    else:
        data = {
            mutation_name: {
                "code": 200,
                "success": success,
                "message": "",
                "error": None,
            }
        }
        if id_value is not None:
            if nested_id_field:
                data[mutation_name]["data"] = {nested_id_field: id_value}
            else:
                data[mutation_name]["id"] = id_value
        resp.json.return_value = {"data": data}
    return resp


def _graphql_query_response(
    query_name, array_field, records=None, success=True, errors=None
):
    """Build a mock GraphQL query response for get_records.

    Args:
        query_name: Name of the query (e.g., getAllDoctors).
        array_field: Field name for the records array.
        records: List of record dicts.
        success: Whether the query succeeded.
        errors: Optional list of error dicts.

    Returns:
        Mock response object with .json() method.
    """
    resp = mock.MagicMock()
    if errors:
        resp.json.return_value = {"errors": errors}
    else:
        data = {
            query_name: {
                "code": 200,
                "success": success,
                "message": "",
                "error": None,
                array_field: records or [],
            }
        }
        resp.json.return_value = {"data": data}
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

    # --- add_record ---

    def test_add_record_doctor_returns_id(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createFamilyDoctor", success=True, id_value=42, nested_id_field="doctorId"
        )
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.assertEqual(rid, 42)

    def test_add_record_medication_returns_id(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createMedicationAndAllergy", success=True, id_value=7
        )
        rid = self.storage.add_record(
            "alice", "medication", {"name_of_medicine": "Aspirin"}
        )
        self.assertEqual(rid, 7)

    def test_add_record_graphql_error_returns_none(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createFamilyDoctor", errors=[{"message": "something went wrong"}]
        )
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.assertIsNone(rid)

    def test_add_record_mutation_failure_returns_none(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createFamilyDoctor", success=False, id_value=None
        )
        rid = self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        self.assertIsNone(rid)

    def test_add_record_doctor_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createFamilyDoctor", success=True, id_value=1, nested_id_field="doctorId"
        )
        self.storage.add_record(
            "alice", "doctor", {"doctor_name": "Dr. Smith", "location": "123 Main St"}
        )
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        self.assertIn("query", body)
        self.assertIn("variables", body)
        variables = body["variables"]["input"]
        self.assertEqual(variables["userId"], "alice")
        self.assertEqual(variables["doctorName"], "Dr. Smith")
        self.assertEqual(variables["contactInformation"], "123 Main St")

    def test_add_record_medication_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createMedicationAndAllergy", success=True, id_value=2
        )
        self.storage.add_record(
            "alice",
            "medication",
            {
                "name_of_medicine": "Ibuprofen",
                "side_effect": "Nausea",
            },
        )
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["userId"], "alice")
        self.assertEqual(variables["medicineName"], "Ibuprofen")
        self.assertEqual(variables["sideEffect"], "Nausea")
        self.assertEqual(variables["medicationFiles"], [])

    def test_add_record_insurance_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createHealthInsurance", success=True, id_value=3
        )
        self.storage.add_record(
            "alice",
            "insurance",
            {"type_of_health_insurance": "PPO"},
        )
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["userId"], "alice")
        self.assertEqual(variables["memberName"], "PPO")
        self.assertEqual(variables["insuranceTypeId"], 1)
        self.assertEqual(variables["dependents"], [])
        self.assertEqual(variables["files"], [])

    def test_add_record_medical_history_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createMedicalHistories", success=True, id_value=4
        )
        self.storage.add_record(
            "alice",
            "medical_history",
            {"disease": "Hypertension", "description": "Stage 1"},
        )
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["userId"], "alice")
        self.assertEqual(variables["generalHealth"], "Hypertension - Stage 1")
        self.assertEqual(variables["createdBy"], "alice")
        self.assertEqual(variables["userName"], "alice")
        self.assertEqual(variables["responses"], [])

    def test_add_record_medical_history_without_description(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createMedicalHistories", success=True, id_value=5
        )
        self.storage.add_record(
            "alice",
            "medical_history",
            {"disease": "Diabetes"},
        )
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["generalHealth"], "Diabetes")

    def test_add_record_posts_to_graphql_endpoint(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createFamilyDoctor", success=True, id_value=1, nested_id_field="doctorId"
        )
        self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        call_args = self.session.post.call_args
        url = call_args[0][0]
        self.assertTrue(url.endswith("/graphql"))

    # --- get_records ---

    def test_get_records_returns_normalized_doctor_list(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getAllDoctors",
            "doctor",
            [
                {
                    "doctorId": 1,
                    "userId": "alice",
                    "doctorName": "Dr. A",
                    "contact": "123 Main",
                }
            ],
        )
        records = self.storage.get_records("alice", record_type="doctor")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 1)
        self.assertEqual(records[0]["username"], "alice")
        self.assertEqual(records[0]["payload"]["doctor_name"], "Dr. A")
        self.assertEqual(records[0]["payload"]["location"], "123 Main")

    def test_get_records_returns_normalized_medication_list(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getMedicationsByUserId",
            "data",
            [
                {
                    "medicationId": 2,
                    "userId": "alice",
                    "medicineName": "Aspirin",
                    "purpose": "Pain relief",
                    "sideEffect": "None",
                }
            ],
        )
        records = self.storage.get_records("alice", record_type="medication")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 2)
        self.assertEqual(records[0]["payload"]["name_of_medicine"], "Aspirin")
        self.assertEqual(records[0]["payload"]["purpose"], "Pain relief")
        self.assertEqual(records[0]["payload"]["side_effect"], "None")

    def test_get_records_returns_empty_on_graphql_error(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getAllDoctors", "doctor", errors=[{"message": "failed"}]
        )
        records = self.storage.get_records("alice", record_type="doctor")
        self.assertEqual(len(records), 0)

    def test_get_records_returns_empty_on_query_failure(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getAllDoctors", "doctor", success=False
        )
        records = self.storage.get_records("alice", record_type="doctor")
        self.assertEqual(len(records), 0)

    def test_get_records_sends_userId_variable(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getAllDoctors", "doctor", []
        )
        self.storage.get_records("alice", record_type="doctor")
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]
        self.assertEqual(variables["userId"], "alice")

    def test_get_records_filters_by_id(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getAllDoctors",
            "doctor",
            [
                {
                    "doctorId": 1,
                    "userId": "alice",
                    "doctorName": "Dr. A",
                    "contact": "",
                },
                {
                    "doctorId": 2,
                    "userId": "alice",
                    "doctorName": "Dr. B",
                    "contact": "",
                },
            ],
        )
        records = self.storage.get_records("alice", record_type="doctor", id=2)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 2)

    # --- update_record ---

    def test_update_record_doctor_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "updateFamilyDoctor", success=True
        )
        ok = self.storage.update_record(
            10,
            {"doctor_name": "Dr. New", "location": "456 Oak"},
            record_type="doctor",
            username="alice",
        )
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["doctorId"], 10)
        self.assertEqual(variables["userId"], "alice")
        self.assertEqual(variables["doctorName"], "Dr. New")
        self.assertEqual(variables["contactInformation"], "456 Oak")

    def test_update_record_medication_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "updateMedicationAndAllergies", success=True
        )
        ok = self.storage.update_record(
            5,
            {"name_of_medicine": "Tylenol", "side_effect": "Drowsiness"},
            record_type="medication",
            username="alice",
        )
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["recordId"], 5)
        self.assertEqual(variables["medication"], "Tylenol")
        self.assertEqual(variables["allergy"], "Drowsiness")

    def test_update_record_insurance_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "updateHealthInsurance", success=True
        )
        ok = self.storage.update_record(
            3,
            {"type_of_health_insurance": "HMO"},
            record_type="insurance",
            username="alice",
        )
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["insuranceId"], 3)
        self.assertEqual(variables["insuranceName"], "HMO")

    def test_update_record_medical_history_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "updateMedicalHistory", success=True
        )
        ok = self.storage.update_record(
            8,
            {"disease": "Asthma", "description": "Mild"},
            record_type="medical_history",
            username="alice",
        )
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["historyId"], 8)
        self.assertEqual(variables["history"], "Asthma - Mild")

    def test_update_record_returns_false_on_graphql_error(self) -> None:
        self.session.post.return_value = _graphql_response(
            "updateFamilyDoctor", errors=[{"message": "failed"}]
        )
        ok = self.storage.update_record(
            10, {"doctor_name": "Dr. New"}, record_type="doctor", username="alice"
        )
        self.assertFalse(ok)

    def test_update_record_returns_false_on_mutation_failure(self) -> None:
        self.session.post.return_value = _graphql_response(
            "updateFamilyDoctor", success=False
        )
        ok = self.storage.update_record(
            10, {"doctor_name": "Dr. New"}, record_type="doctor", username="alice"
        )
        self.assertFalse(ok)

    # --- delete_record ---

    def test_delete_record_doctor_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteDoctorDetails", success=True
        )
        ok = self.storage.delete_record(10, record_type="doctor", username="alice")
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["id"], 10)
        self.assertEqual(variables["userId"], "alice")

    def test_delete_record_medication_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteMedicationAllergies", success=True
        )
        ok = self.storage.delete_record(5, record_type="medication", username="alice")
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["id"], 5)
        self.assertEqual(variables["userId"], "alice")

    def test_delete_record_insurance_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteHealthInsurance", success=True
        )
        ok = self.storage.delete_record(3, record_type="insurance", username="alice")
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["id"], 3)
        self.assertEqual(variables["userId"], "alice")

    def test_delete_record_medical_history_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteMedicalHistory", success=True
        )
        ok = self.storage.delete_record(
            8, record_type="medical_history", username="alice"
        )
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        variables = body["variables"]["input"]
        self.assertEqual(variables["id"], 8)
        self.assertEqual(variables["userId"], "alice")

    def test_delete_record_returns_false_on_graphql_error(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteDoctorDetails", errors=[{"message": "failed"}]
        )
        ok = self.storage.delete_record(10, record_type="doctor", username="alice")
        self.assertFalse(ok)

    def test_delete_record_returns_false_on_mutation_failure(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteDoctorDetails", success=False
        )
        ok = self.storage.delete_record(10, record_type="doctor", username="alice")
        self.assertFalse(ok)

    # --- correlation ID ---

    def test_request_includes_correlation_id(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getAllDoctors", "doctor", []
        )
        self.storage.get_records("alice", record_type="doctor")
        _, kwargs = self.session.post.call_args
        self.assertIn("headers", kwargs)
        self.assertIn("X-Correlation-ID", kwargs["headers"])

    # --- GraphQL request structure ---

    def test_request_body_has_query_and_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createFamilyDoctor", success=True, id_value=1
        )
        self.storage.add_record("alice", "doctor", {"doctor_name": "Dr. A"})
        _, kwargs = self.session.post.call_args
        body = kwargs["json"]
        self.assertIn("query", body)
        self.assertIn("variables", body)
        self.assertIsInstance(body["query"], str)
        self.assertIsInstance(body["variables"], dict)

    # --- education add_record ---

    def test_add_record_education_returns_id(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createEducation", success=True, id_value=20
        )
        rid = self.storage.add_record(
            "alice",
            "education",
            {"institution": "State University", "degree": "B.Sc. Computer Science"},
        )
        self.assertEqual(rid, 20)

    def test_add_record_education_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createEducation", success=True, id_value=20
        )
        self.storage.add_record(
            "alice",
            "education",
            {
                "institution": "State University",
                "degree": "B.Sc. Computer Science",
                "is_currently_pursuing": True,
            },
        )
        _, kwargs = self.session.post.call_args
        variables = kwargs["json"]["variables"]["input"]
        self.assertEqual(variables["userId"], "alice")
        self.assertEqual(variables["universityOrCollegeName"], "State University")
        self.assertEqual(variables["educationCertificateName"], "B.Sc. Computer Science")
        self.assertTrue(variables["isCurrentlyPursuing"])
        self.assertEqual(variables["createdBy"], "alice")
        self.assertEqual(variables["files"], [])

    # --- contact add_record ---

    def test_add_record_contact_returns_id(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createContact", success=True, id_value=30
        )
        rid = self.storage.add_record(
            "alice",
            "contact",
            {"name": "Jane Doe", "relationship": "friend"},
        )
        self.assertEqual(rid, 30)

    def test_add_record_contact_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createContact", success=True, id_value=30
        )
        self.storage.add_record(
            "alice",
            "contact",
            {
                "name": "Jane Doe",
                "relationship": "friend",
                "phone": "555-1234",
                "email": "jane@example.com",
            },
        )
        _, kwargs = self.session.post.call_args
        variables = kwargs["json"]["variables"]["input"]
        self.assertEqual(variables["userId"], "alice")
        self.assertEqual(variables["name"], "Jane Doe")
        self.assertEqual(variables["relationship"], "friend")
        self.assertEqual(variables["contactNumber"], "555-1234")
        self.assertEqual(variables["emailId"], "jane@example.com")
        self.assertIsInstance(variables["contactTypeId"], list)

    # --- attorney add_record ---

    def test_add_record_attorney_returns_id(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createContact", success=True, id_value=31
        )
        rid = self.storage.add_record(
            "alice",
            "attorney",
            {"name": "Sarah Morgan", "specialty": "Estate Planning"},
        )
        self.assertEqual(rid, 31)

    def test_add_record_attorney_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "createContact", success=True, id_value=31
        )
        self.storage.add_record(
            "alice",
            "attorney",
            {"name": "Sarah Morgan", "email": "s.morgan@law.com"},
        )
        _, kwargs = self.session.post.call_args
        variables = kwargs["json"]["variables"]["input"]
        self.assertEqual(variables["userId"], "alice")
        self.assertEqual(variables["name"], "Sarah Morgan")
        self.assertEqual(variables["emailId"], "s.morgan@law.com")
        self.assertIsInstance(variables["contactTypeId"], list)

    # --- education / contact get_records ---

    def test_get_records_returns_normalized_education_list(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getEducationByUserId",
            "education",
            [
                {
                    "educationId": 20,
                    "userId": "alice",
                    "educationCertificateName": "B.Sc. CS",
                    "universityOrCollegeName": "State U",
                    "isCurrentlyPursuing": False,
                }
            ],
        )
        records = self.storage.get_records("alice", record_type="education")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 20)
        self.assertEqual(records[0]["payload"]["degree"], "B.Sc. CS")
        self.assertEqual(records[0]["payload"]["institution"], "State U")

    def test_get_records_returns_normalized_contact_list(self) -> None:
        self.session.post.return_value = _graphql_query_response(
            "getContactByUserId",
            "contacts",
            [
                {
                    "contactId": 30,
                    "userId": "alice",
                    "name": "Jane Doe",
                    "relationship": "friend",
                    "contactNumber": "555-1234",
                    "emailId": "jane@example.com",
                }
            ],
        )
        records = self.storage.get_records("alice", record_type="contact")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 30)
        self.assertEqual(records[0]["payload"]["name"], "Jane Doe")
        self.assertEqual(records[0]["payload"]["relationship"], "friend")
        self.assertEqual(records[0]["payload"]["phone"], "555-1234")
        self.assertEqual(records[0]["payload"]["email"], "jane@example.com")

    # --- education / contact delete_record ---

    def test_delete_record_education_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteEducationById", success=True
        )
        ok = self.storage.delete_record(20, record_type="education", username="alice")
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        variables = kwargs["json"]["variables"]["input"]
        self.assertEqual(variables["id"], 20)
        self.assertEqual(variables["userId"], "alice")

    def test_delete_record_contact_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteContact", success=True
        )
        ok = self.storage.delete_record(30, record_type="contact", username="alice")
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        # deleteContact uses direct args, not an input wrapper
        variables = kwargs["json"]["variables"]
        self.assertEqual(variables["id"], [30])
        self.assertEqual(variables["userId"], "alice")

    def test_delete_record_attorney_sends_correct_variables(self) -> None:
        self.session.post.return_value = _graphql_response(
            "deleteContact", success=True
        )
        ok = self.storage.delete_record(31, record_type="attorney", username="alice")
        self.assertTrue(ok)
        _, kwargs = self.session.post.call_args
        # deleteContact uses direct args, not an input wrapper
        variables = kwargs["json"]["variables"]
        self.assertEqual(variables["id"], [31])
        self.assertEqual(variables["userId"], "alice")
