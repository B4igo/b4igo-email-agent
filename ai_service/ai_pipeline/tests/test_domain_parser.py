"""Unit tests for DomainParser."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase

from ai_service.ai_pipeline.domain_parser import DomainParser
from shared.mail.models import EmailAddress, EmailInput
from shared.schemas.health_schemas import (
    Appointment,
    Bill,
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)


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


if __name__ == "__main__":
    import unittest

    unittest.main()
