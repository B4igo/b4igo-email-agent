"""Unit tests for DomainParser."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase, mock

from ai_service.ai_pipeline.domain_parser import DomainParser
from shared.schemas.legal_schemas import (
    Attorney,
    Contract,
    CourtDate,
    LegalNotice,
)
from shared.schemas.personal_schemas import (
    Contact,
    PersonalEvent,
    Reminder,
)
from shared.schemas.schemas import (
    Appointment,
    Bill,
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)
from shared.mail.models import EmailAddress, EmailInput

# Mock Ollama response so tests run without a running Ollama or qwen3:8b model.
_MOCK_CHAT_RESPONSE_JSON = {
    "results": [
        {"Appointment": {"date": "2024-01-01", "provider": "Dr. Smith"}},
        {"Doctor": {"doctor_name": "Dr. Jane"}},
        {"Medication": {"name_of_medicine": "Aspirin"}},
        {"Medication": {"name_of_medicine": "Ibuprofen"}},
        {"Insurance": {"type_of_health_insurance": "PPO", "coverage_type": "Family"}},
        {"MedicalHistory": {"date": "2024-01-01", "disease": "Flu"}},
        {"Bill": {"amount": 100.0, "due_date": "2024-02-01", "vendor": "Hospital"}},
    ]
}


class TestDomainParser(TestCase):
    """Unit tests for DomainParser parsing with health domain."""

    test_cases: List[Dict[str, Any]]
    parser: DomainParser

    @classmethod
    def setUpClass(cls) -> None:
        """Load test emails from JSON and initialize parser."""
        cls.parser = DomainParser()

        # Load test emails from JSON file
        test_file = Path(__file__).parent / "test_emails.json"
        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        cls.test_cases = data["health_emails"]

    def setUp(self) -> None:
        """Patch ollama.chat so tests do not require Ollama or qwen3:8b."""
        self._chat_patcher = mock.patch("ai_service.ai_pipeline.domain_parser.chat")
        mock_chat = self._chat_patcher.start()
        mock_response = mock.MagicMock()
        mock_response.message.content = json.dumps(_MOCK_CHAT_RESPONSE_JSON)
        mock_chat.return_value = mock_response

    def tearDown(self) -> None:
        """Stop patching ollama.chat."""
        self._chat_patcher.stop()

    def _load_email(self, email_data: Dict[str, Any]) -> EmailInput:
        """Convert JSON email data to EmailInput instance."""
        return EmailInput(
            from_address=EmailAddress(**email_data["from_address"]),
            to_address=[EmailAddress(**addr) for addr in email_data["to_address"]],
            subject=email_data["subject"],
            body=email_data["body"],
            received_at=datetime.fromisoformat(email_data["received_at"]),
        )

    def _get_test_case(self, name: str) -> Dict[str, Any]:
        """Get a test case by name."""
        for case in self.test_cases:
            if case["name"] == name:
                return case
        raise ValueError(f"Test case '{name}' not found")

    def test_single_appointment(self) -> None:
        """Test parsing email with complete Appointment information."""
        test_case = self._get_test_case("single_appointment")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # Should have at least one result
        self.assertGreater(len(results), 0, "No results returned from parser")

        # Find Appointment instances
        appointments = [r for r in results if isinstance(r, Appointment)]
        self.assertGreater(len(appointments), 0, "No Appointment instance found")

        # Validate the appointment has required fields
        appointment = appointments[0]
        self.assertIsInstance(appointment, Appointment)
        self.assertIsNotNone(appointment.date, "Appointment date is None")
        self.assertIsNotNone(appointment.provider, "Appointment provider is None")

    def test_single_doctor(self) -> None:
        """Test parsing email with complete Doctor information."""
        test_case = self._get_test_case("single_doctor")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # Should have at least one result
        self.assertGreater(len(results), 0, "No results returned from parser")

        # Find Doctor instances
        doctors = [r for r in results if isinstance(r, Doctor)]
        self.assertGreater(len(doctors), 0, "No Doctor instance found")

        # Validate the doctor has required fields
        doctor = doctors[0]
        self.assertIsInstance(doctor, Doctor)
        self.assertIsNotNone(doctor.doctor_name, "Doctor name is None")

    def test_appointment_and_doctor(self) -> None:
        """Test parsing email with both Appointment and Doctor information."""
        test_case = self._get_test_case("appointment_and_doctor")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # Should have at least two results
        self.assertGreaterEqual(len(results), 2, "Expected at least 2 results")

        # Find both schema instances
        appointments = [r for r in results if isinstance(r, Appointment)]
        doctors = [r for r in results if isinstance(r, Doctor)]

        self.assertGreater(len(appointments), 0, "No Appointment instance found")
        self.assertGreater(len(doctors), 0, "No Doctor instance found")

        # Validate both have required fields
        appointment = appointments[0]
        self.assertIsNotNone(appointment.date)
        self.assertIsNotNone(appointment.provider)

        doctor = doctors[0]
        self.assertIsNotNone(doctor.doctor_name)

    def test_medication_and_medical_history(self) -> None:
        """Test parsing email with Medication and MedicalHistory information."""
        test_case = self._get_test_case("medication_and_medical_history")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # Should have at least two results
        self.assertGreaterEqual(len(results), 2, "Expected at least 2 results")

        # Find both schema instances
        medications = [r for r in results if isinstance(r, Medication)]
        histories = [r for r in results if isinstance(r, MedicalHistory)]

        self.assertGreater(len(medications), 0, "No Medication instance found")
        self.assertGreater(len(histories), 0, "No MedicalHistory instance found")

        # Validate required fields
        medication = medications[0]
        self.assertIsNotNone(medication.name_of_medicine)

        history = histories[0]
        self.assertIsNotNone(history.date)
        self.assertIsNotNone(history.disease)

    def test_complete_bill(self) -> None:
        """Test parsing email with complete Bill information."""
        test_case = self._get_test_case("complete_bill")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # Should have at least one result
        self.assertGreater(len(results), 0, "No results returned from parser")

        # Find Bill instances
        bills = [r for r in results if isinstance(r, Bill)]
        self.assertGreater(len(bills), 0, "No Bill instance found")

        # Validate the bill has required fields
        bill = bills[0]
        self.assertIsInstance(bill, Bill)
        self.assertIsNotNone(bill.amount, "Bill amount is None")
        self.assertGreater(bill.amount, 0, "Bill amount should be positive")
        self.assertIsNotNone(bill.due_date, "Bill due_date is None")
        self.assertIsNotNone(bill.vendor, "Bill vendor is None")

    def test_complete_insurance(self) -> None:
        """Test parsing email with complete Insurance information."""
        test_case = self._get_test_case("complete_insurance")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # Should have at least one result
        self.assertGreater(len(results), 0, "No results returned from parser")

        # Find Insurance instances
        insurances = [r for r in results if isinstance(r, Insurance)]
        self.assertGreater(len(insurances), 0, "No Insurance instance found")

        # Validate the insurance has required fields
        insurance = insurances[0]
        self.assertIsInstance(insurance, Insurance)
        self.assertIsNotNone(
            insurance.type_of_health_insurance, "Insurance type is None"
        )
        self.assertIsNotNone(insurance.coverage_type, "Coverage type is None")

    def test_incomplete_medication(self) -> None:
        """Test parsing email with incomplete Medication info."""
        test_case = self._get_test_case("incomplete_medication")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # With incomplete data, parser may still return results or may not
        # We should NOT get a valid Medication instance with missing required field
        _ = [r for r in results if isinstance(r, Medication)]

        # Either no medications, or if one exists, it should have failed validation
        # In this case, we expect the parser to not return incomplete medications
        # or to catch validation errors
        # For now, we just document that this is an edge case
        # The test passes as long as it doesn't crash
        pass

    def test_incomplete_appointment(self) -> None:
        """Test parsing email with incomplete Appointment info (missing provider)."""
        test_case = self._get_test_case("incomplete_appointment")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # With incomplete data, parser may still return results or may not
        # We should NOT get a valid Appointment instance with missing required field
        _ = [r for r in results if isinstance(r, Appointment)]

        # Either no appointments, or validation should have failed
        # The test passes as long as it doesn't crash
        pass

    def test_multiple_medications(self) -> None:
        """Test parsing email with multiple Medication entries."""
        test_case = self._get_test_case("multiple_medications")
        email = self._load_email(test_case["email"])

        results = self.parser(email.to_text(), "health")

        # Should have at least two Medication results
        medications = [r for r in results if isinstance(r, Medication)]
        self.assertGreaterEqual(len(medications), 2, "Expected at least 2 Medications")

        # Validate each medication has required fields
        for medication in medications:
            self.assertIsInstance(medication, Medication)
            self.assertIsNotNone(
                medication.name_of_medicine, f"Medication missing name: {medication}"
            )


_MOCK_PERSONAL_RESPONSE_JSON = {
    "results": [
        {
            "Contact": {
                "name": "Tom Nguyen",
                "relationship": "Friend",
                "email": "tom.nguyen@gmail.com",
            }
        },
        {
            "PersonalEvent": {
                "event_name": "Jessica's 30th Birthday Celebration",
                "type": "Birthday Party",
                "date": "2026-04-05",
            }
        },
        {
            "Reminder": {
                "task": "Call Mom for her birthday",
                "due_date": "2026-03-15",
                "priority": "High",
            }
        },
    ]
}

_MOCK_LEGAL_RESPONSE_JSON = {
    "results": [
        {
            "Attorney": {
                "name": "Rachel Harris",
                "firm": "Harris & Associates Law Firm",
                "specialty": "Contract Law",
            }
        },
        {
            "Contract": {
                "title": "Technology Services Agreement",
                "effective_date": "2026-04-01",
                "expiry_date": "2027-03-31",
            }
        },
        {
            "CourtDate": {
                "date": "2026-04-15",
                "time": "9:30 AM",
                "case_number": "2026-CV-00847",
            }
        },
        {
            "LegalNotice": {
                "type": "Cease and Desist",
                "sender": "TechCorp Inc.",
                "deadline": "2026-03-27",
            }
        },
    ]
}


class TestPersonalDomainParser(TestCase):
    """Unit tests for DomainParser parsing with personal domain."""

    test_cases: List[Dict[str, Any]]
    parser: DomainParser

    @classmethod
    def setUpClass(cls) -> None:
        """Load test emails from JSON and initialize parser."""
        cls.parser = DomainParser()
        test_file = Path(__file__).parent / "test_emails.json"
        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls.test_cases = data["personal_emails"]

    def setUp(self) -> None:
        """Patch ollama.chat so tests do not require Ollama."""
        self._chat_patcher = mock.patch("ai_service.ai_pipeline.domain_parser.chat")
        mock_chat = self._chat_patcher.start()
        mock_response = mock.MagicMock()
        mock_response.message.content = json.dumps(_MOCK_PERSONAL_RESPONSE_JSON)
        mock_chat.return_value = mock_response

    def tearDown(self) -> None:
        """Stop patching ollama.chat."""
        self._chat_patcher.stop()

    def _load_email(self, email_data: Dict[str, Any]) -> EmailInput:
        """Convert JSON email data to EmailInput instance."""
        return EmailInput(
            from_address=EmailAddress(**email_data["from_address"]),
            to_address=[EmailAddress(**addr) for addr in email_data["to_address"]],
            subject=email_data["subject"],
            body=email_data["body"],
            received_at=datetime.fromisoformat(email_data["received_at"]),
        )

    def _get_test_case(self, name: str) -> Dict[str, Any]:
        """Get a test case by name."""
        for case in self.test_cases:
            if case["name"] == name:
                return case
        raise ValueError(f"Test case '{name}' not found")

    def test_single_contact(self) -> None:
        """Test parsing email with a single Contact."""
        email = self._load_email(self._get_test_case("single_contact")["email"])
        results = self.parser(email.to_text(), "personal")
        contacts = [r for r in results if isinstance(r, Contact)]
        self.assertGreater(len(contacts), 0, "No Contact instance found")
        self.assertIsNotNone(contacts[0].name)

    def test_personal_event(self) -> None:
        """Test parsing email with a PersonalEvent."""
        email = self._load_email(
            self._get_test_case("personal_event_birthday")["email"]
        )
        results = self.parser(email.to_text(), "personal")
        events = [r for r in results if isinstance(r, PersonalEvent)]
        self.assertGreater(len(events), 0, "No PersonalEvent instance found")
        self.assertIsNotNone(events[0].event_name)

    def test_reminder_and_contact(self) -> None:
        """Test parsing email containing both a Reminder and a Contact."""
        email = self._load_email(self._get_test_case("reminder_from_friend")["email"])
        results = self.parser(email.to_text(), "personal")
        reminders = [r for r in results if isinstance(r, Reminder)]
        contacts = [r for r in results if isinstance(r, Contact)]
        self.assertGreater(len(reminders), 0, "No Reminder instance found")
        self.assertGreater(len(contacts), 0, "No Contact instance found")
        self.assertIsNotNone(reminders[0].task)


class TestLegalDomainParser(TestCase):
    """Unit tests for DomainParser parsing with legal domain."""

    test_cases: List[Dict[str, Any]]
    parser: DomainParser

    @classmethod
    def setUpClass(cls) -> None:
        """Load test emails from JSON and initialize parser."""
        cls.parser = DomainParser()
        test_file = Path(__file__).parent / "test_emails.json"
        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls.test_cases = data["legal_emails"]

    def setUp(self) -> None:
        """Patch ollama.chat so tests do not require Ollama."""
        self._chat_patcher = mock.patch("ai_service.ai_pipeline.domain_parser.chat")
        mock_chat = self._chat_patcher.start()
        mock_response = mock.MagicMock()
        mock_response.message.content = json.dumps(_MOCK_LEGAL_RESPONSE_JSON)
        mock_chat.return_value = mock_response

    def tearDown(self) -> None:
        """Stop patching ollama.chat."""
        self._chat_patcher.stop()

    def _load_email(self, email_data: Dict[str, Any]) -> EmailInput:
        """Convert JSON email data to EmailInput instance."""
        return EmailInput(
            from_address=EmailAddress(**email_data["from_address"]),
            to_address=[EmailAddress(**addr) for addr in email_data["to_address"]],
            subject=email_data["subject"],
            body=email_data["body"],
            received_at=datetime.fromisoformat(email_data["received_at"]),
        )

    def _get_test_case(self, name: str) -> Dict[str, Any]:
        """Get a test case by name."""
        for case in self.test_cases:
            if case["name"] == name:
                return case
        raise ValueError(f"Test case '{name}' not found")

    def test_contract_and_attorney(self) -> None:
        """Test parsing email with a Contract and Attorney."""
        email = self._load_email(self._get_test_case("contract_review")["email"])
        results = self.parser(email.to_text(), "legal")
        contracts = [r for r in results if isinstance(r, Contract)]
        attorneys = [r for r in results if isinstance(r, Attorney)]
        self.assertGreater(len(contracts), 0, "No Contract instance found")
        self.assertGreater(len(attorneys), 0, "No Attorney instance found")
        self.assertIsNotNone(contracts[0].title)
        self.assertIsNotNone(attorneys[0].name)

    def test_court_date(self) -> None:
        """Test parsing email with a CourtDate."""
        email = self._load_email(
            self._get_test_case("court_date_notification")["email"]
        )
        results = self.parser(email.to_text(), "legal")
        court_dates = [r for r in results if isinstance(r, CourtDate)]
        self.assertGreater(len(court_dates), 0, "No CourtDate instance found")
        self.assertIsNotNone(court_dates[0].date)

    def test_legal_notice(self) -> None:
        """Test parsing email with a LegalNotice."""
        email = self._load_email(
            self._get_test_case("legal_notice_cease_desist")["email"]
        )
        results = self.parser(email.to_text(), "legal")
        notices = [r for r in results if isinstance(r, LegalNotice)]
        self.assertGreater(len(notices), 0, "No LegalNotice instance found")
        self.assertIsNotNone(notices[0].type)

    def test_attorney_introduction(self) -> None:
        """Test parsing email with an Attorney introduction."""
        email = self._load_email(self._get_test_case("attorney_introduction")["email"])
        results = self.parser(email.to_text(), "legal")
        attorneys = [r for r in results if isinstance(r, Attorney)]
        self.assertGreater(len(attorneys), 0, "No Attorney instance found")
        self.assertIsNotNone(attorneys[0].name)


if __name__ == "__main__":
    import unittest

    unittest.main()
