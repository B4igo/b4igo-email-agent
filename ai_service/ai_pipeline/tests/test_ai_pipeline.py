"""Integration tests for the AI pipeline: domain classification and schema extraction.

Each test loads a scenario from shared/scenarios/, classifies its domain, parses it
for structured entries, and checks the results against expected schema types and field
values embedded in the scenario's "expected" block.

Statistics printed at teardown:
  - Domain classification accuracy
  - Schema extraction accuracy
  - Required-field extraction rate (fields explicitly planted in the body)
  - Optional-field extraction rate (harder fields also planted in the body)

Confidence threshold: the classifier itself promotes low-confidence results to "other"
using DomainClassifier.CONFIDENCE_THRESHOLD. Tune that value on the classifier if too
many legitimate emails are rejected, or too many spam/system emails bleed through.
"""

import json
from pathlib import Path
from typing import Any
from unittest import TestCase

from ai_service.ai_pipeline.ai_pipeline import AIPipeline
from shared.attachment_utils import append_attachments_to_text
from shared.schemas.health_schemas import (
    Appointment,
    Bill,
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)
from shared.schemas.legal_schemas import Attorney, Contract, CourtDate, LegalNotice
from shared.schemas.personal_schemas import Contact, PersonalEvent, Reminder

SCENARIOS_DIR = Path(__file__).parent.parent.parent.parent / "shared" / "scenarios"


class TestAIPipeline(TestCase):
    """End-to-end tests: scenario file → classify → parse → assert fields."""

    pipeline: AIPipeline

    _stats: dict[str, int] = {
        "domains_tested": 0,
        "domains_correct": 0,
        "schemas_tested": 0,
        "schemas_correct": 0,
        "required_fields_total": 0,
        "required_fields_found": 0,
        "optional_fields_total": 0,
        "optional_fields_found": 0,
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.pipeline = AIPipeline()

    @classmethod
    def tearDownClass(cls) -> None:
        s = cls._stats
        lines = ["\n=== AI Pipeline Test Statistics ==="]
        if s["domains_tested"]:
            pct = 100 * s["domains_correct"] // s["domains_tested"]
            lines.append(
                f"  Domain classification : {s['domains_correct']}/{s['domains_tested']}  ({pct}%)"
            )
        if s["schemas_tested"]:
            pct = 100 * s["schemas_correct"] // s["schemas_tested"]
            lines.append(
                f"  Schema extraction     : {s['schemas_correct']}/{s['schemas_tested']}  ({pct}%)"
            )
        if s["required_fields_total"]:
            pct = 100 * s["required_fields_found"] // s["required_fields_total"]
            lines.append(
                f"  Required fields       : {s['required_fields_found']}/{s['required_fields_total']}  ({pct}%)"
            )
        if s["optional_fields_total"]:
            pct = 100 * s["optional_fields_found"] // s["optional_fields_total"]
            lines.append(
                f"  Optional fields       : {s['optional_fields_found']}/{s['optional_fields_total']}  ({pct}%)"
            )
        print("\n".join(lines))

    # ── helpers ───────────────────────────────────────────────────────────────

    def _load(self, filename: str) -> dict[str, Any]:
        path = SCENARIOS_DIR / filename
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _text(scenario: dict[str, Any]) -> str:
        """Build classifier/parser input from scenario subject + body."""
        parts: list[str] = []
        if scenario.get("subject"):
            parts.append(f"Subject: {scenario['subject']}")
        if scenario.get("body"):
            parts.append(scenario["body"])
        return "\n\n".join(parts)

    def _classify(self, scenario_file: str) -> tuple[str, float, dict[str, float]]:
        data = self._load(scenario_file)
        result = self.pipeline.domain_classifier(self._text(data))
        return result["domain"], result["confidence"], result["all_scores"]

    def _parse(self, scenario_file: str, domain: str) -> list:
        data = self._load(scenario_file)
        return self.pipeline.domain_parser(self._text(data), domain)

    def _text_with_attachments(self, scenario_file: str) -> str:
        """Build text from scenario body + docling-converted attachments.

        Skips the calling test if any listed attachment file does not exist yet.
        """
        data = self._load(scenario_file)
        text = self._text(data)
        attachment_paths = [SCENARIOS_DIR / rel for rel in data.get("attachments", [])]
        missing = [p for p in attachment_paths if not p.exists()]
        if missing:
            self.skipTest(
                f"Attachment file(s) not yet created: {[str(p) for p in missing]}"
            )
        if attachment_paths:
            text = append_attachments_to_text(attachment_paths, text)
        return text

    def _assert_domain(self, scenario_file: str, expected: str) -> tuple[str, float]:
        """Assert classification result, update domain stats, return (domain, confidence)."""
        s = self.__class__._stats
        s["domains_tested"] += 1
        domain, confidence, all_scores = self._classify(scenario_file)
        if domain == expected:
            s["domains_correct"] += 1
        self.assertEqual(
            domain,
            expected,
            f"[{scenario_file}] expected domain='{expected}', got='{domain}' "
            f"(confidence={confidence:.2f}, all={all_scores})",
        )
        return domain, confidence

    def _assert_schema(
        self,
        results: list,
        schema_class: type,
        required: dict[str, Any],
        optional: dict[str, Any] | None = None,
        label: str = "",
    ) -> None:
        """Assert a schema instance was extracted; check required fields; track stats."""
        s = self.__class__._stats
        s["schemas_tested"] += 1

        instances = [r for r in results if isinstance(r, schema_class)]
        self.assertGreater(
            len(instances),
            0,
            f"[{label}] no {schema_class.__name__} found in results "
            f"{[type(r).__name__ for r in results]}",
        )
        s["schemas_correct"] += 1
        obj = instances[0]

        for field, expected_val in required.items():
            s["required_fields_total"] += 1
            actual = getattr(obj, field, None)
            self.assertIsNotNone(
                actual, f"[{label}] {schema_class.__name__}.{field} is None"
            )
            if isinstance(expected_val, str) and isinstance(actual, str):
                self.assertIn(
                    expected_val.lower(),
                    actual.lower(),
                    f"[{label}] {schema_class.__name__}.{field}='{actual}', "
                    f"expected substring '{expected_val}'",
                )
            elif isinstance(expected_val, float):
                self.assertAlmostEqual(
                    float(actual),
                    expected_val,
                    places=2,
                    msg=f"[{label}] {schema_class.__name__}.{field}={actual}, "
                    f"expected ~{expected_val}",
                )
            s["required_fields_found"] += 1

        for field, expected_val in (optional or {}).items():
            s["optional_fields_total"] += 1
            actual = getattr(obj, field, None)
            if actual is None:
                continue
            if isinstance(expected_val, str) and isinstance(actual, str):
                if expected_val.lower() in actual.lower():
                    s["optional_fields_found"] += 1
            elif expected_val is None or not isinstance(
                expected_val, (str, int, float)
            ):
                s["optional_fields_found"] += 1
            elif isinstance(expected_val, (int, float)):
                if abs(float(actual) - float(expected_val)) < 0.01:
                    s["optional_fields_found"] += 1

    # ── health ────────────────────────────────────────────────────────────────

    def test_health_appointment(self) -> None:
        """Appointment email classifies as health and yields an Appointment entry."""
        self._assert_domain("appointment.json", "health")
        results = self._parse("appointment.json", "health")
        self._assert_schema(
            results,
            Appointment,
            required={"provider": "Eleanor Reyes"},
            optional={
                "time": "10:30",
                "location": "Harbor View",
                "appointment_type": "physical",
                "duration": 45,
            },
            label="appointment",
        )

    def test_health_bill(self) -> None:
        """Medical bill classifies as health and yields a Bill entry."""
        self._assert_domain("bill.json", "health")
        results = self._parse("bill.json", "health")
        self._assert_schema(
            results,
            Bill,
            required={"amount": 347.80, "vendor": "UCSF"},
            optional={
                "due_date": "2026-04-15",
                "account_number": "UCH-4829-3317",
                "invoice_number": "INV-2026-0391",
            },
            label="bill",
        )

    def test_health_bill_with_attachment(self) -> None:
        """Medical bill with attached statement: classifies as health, extracts Bill from email body."""
        self._assert_domain("bill_with_statement.json", "health")
        results = self._parse("bill_with_statement.json", "health")
        self._assert_schema(
            results,
            Bill,
            required={"amount": 215.50, "vendor": "Eastside Medical"},
            optional={"due_date": "2026-04-28", "account_number": "EMG-7731-02"},
            label="bill_with_statement",
        )

    def test_health_doctor(self) -> None:
        """Doctor welcome email classifies as health and yields a Doctor entry."""
        self._assert_domain("doctor.json", "health")
        results = self._parse("doctor.json", "health")
        self._assert_schema(
            results,
            Doctor,
            required={"doctor_name": "Marcus Webb"},
            optional={"type": "Internal Medicine", "location": "Eastside Medical"},
            label="doctor",
        )

    def test_health_insurance(self) -> None:
        """Insurance enrollment email classifies as health and yields an Insurance entry."""
        self._assert_domain("insurance.json", "health")
        results = self._parse("insurance.json", "health")
        self._assert_schema(
            results,
            Insurance,
            required={"type_of_health_insurance": "PPO", "coverage_type": "Family"},
            optional={"last_updated": "2026"},
            label="insurance",
        )

    def test_health_medication(self) -> None:
        """Prescription-ready email classifies as health and yields a Medication entry."""
        self._assert_domain("medication.json", "health")
        results = self._parse("medication.json", "health")
        self._assert_schema(
            results,
            Medication,
            required={"name_of_medicine": "Metformin"},
            optional={"purpose": "diabetes", "duration": "90", "date": "2026-03-20"},
            label="medication",
        )

    def test_health_medical_history(self) -> None:
        """Patient portal diagnosis email classifies as health and yields a MedicalHistory entry."""
        self._assert_domain("medical_history.json", "health")
        results = self._parse("medical_history.json", "health")
        self._assert_schema(
            results,
            MedicalHistory,
            required={"disease": "Hypertension", "date": "2026"},
            optional={"description": "blood pressure"},
            label="medical_history",
        )

    # ── legal ─────────────────────────────────────────────────────────────────

    def test_legal_jury_duty_court_date(self) -> None:
        """Jury duty summons classifies as legal and yields a CourtDate entry."""
        self._assert_domain("jury_duty.json", "legal")
        results = self._parse("jury_duty.json", "legal")
        self._assert_schema(
            results,
            CourtDate,
            required={"court": "Alameda"},
            optional={"date": "2026", "case_type": "jury"},
            label="jury_duty (CourtDate)",
        )

    def test_legal_jury_duty_notice(self) -> None:
        """Jury duty summons also yields a LegalNotice entry (same scenario, same parse call)."""
        results = self._parse("jury_duty.json", "legal")
        self._assert_schema(
            results,
            LegalNotice,
            required={"type": "summons"},
            optional={"sender": "Alameda", "deadline": "2026"},
            label="jury_duty (LegalNotice)",
        )

    def test_legal_attorney(self) -> None:
        """Attorney engagement letter classifies as legal and yields an Attorney entry."""
        self._assert_domain("attorney.json", "legal")
        results = self._parse("attorney.json", "legal")
        self._assert_schema(
            results,
            Attorney,
            required={"name": "Patricia Nguyen"},
            optional={
                "firm": "Nguyen",
                "specialty": "Contract",
                "email": "pnguyen@nguyenlaw.com",
                "phone": "415",
            },
            label="attorney",
        )

    def test_legal_contract(self) -> None:
        """Contract review email classifies as legal and yields a Contract entry."""
        self._assert_domain("contract_review.json", "legal")
        results = self._parse("contract_review.json", "legal")
        self._assert_schema(
            results,
            Contract,
            required={"title": "Consulting Services Agreement"},
            optional={
                "effective_date": "2026-05-01",
                "expiry_date": "2027-04-30",
                "description": "software",
            },
            label="contract_review",
        )

    def test_legal_court_date(self) -> None:
        """Civil court hearing notice classifies as legal and yields a CourtDate entry."""
        self._assert_domain("court_date.json", "legal")
        results = self._parse("court_date.json", "legal")
        self._assert_schema(
            results,
            CourtDate,
            required={"date": "2026", "court": "Alameda"},
            optional={
                "time": "9:30",
                "case_number": "CV-2026-04178",
                "case_type": "Civil",
            },
            label="court_date",
        )

    def test_legal_notice(self) -> None:
        """HOA compliance notice classifies as legal and yields a LegalNotice entry."""
        self._assert_domain("legal_notice.json", "legal")
        results = self._parse("legal_notice.json", "legal")
        self._assert_schema(
            results,
            LegalNotice,
            required={"type": "Compliance"},
            optional={
                "sender": "Sunrise Ridge",
                "date": "2026-03-15",
                "subject": "Parking",
                "deadline": "2026-04-01",
            },
            label="legal_notice",
        )

    # ── personal ──────────────────────────────────────────────────────────────

    def test_personal_contact(self) -> None:
        """Introduction email classifies as personal and yields a Contact entry."""
        self._assert_domain("contact_intro.json", "personal")
        results = self._parse("contact_intro.json", "personal")
        self._assert_schema(
            results,
            Contact,
            required={"name": "Jordan Lee"},
            optional={
                "email": "jordan.lee@company.com",
                "phone": "669",
                "relationship": "colleague",
            },
            label="contact_intro",
        )

    def test_personal_event(self) -> None:
        """Birthday invitation classifies as personal and yields a PersonalEvent entry."""
        self._assert_domain("personal_event.json", "personal")
        results = self._parse("personal_event.json", "personal")
        self._assert_schema(
            results,
            PersonalEvent,
            required={"event_name": "Birthday"},
            optional={
                "date": "2026-04-12",
                "time": "7:00",
                "location": "Rooftop Lounge",
                "type": "birthday",
            },
            label="personal_event",
        )

    def test_personal_reminder(self) -> None:
        """Reminder email classifies as personal and yields a Reminder entry."""
        self._assert_domain("reminder.json", "personal")
        results = self._parse("reminder.json", "personal")
        self._assert_schema(
            results,
            Reminder,
            required={"task": "family reunion"},
            optional={
                "due_date": "2026-05-15",
                "priority": "High",
                "category": "Travel",
            },
            label="reminder",
        )

    def test_personal_meeting_event(self) -> None:
        """Meeting reminder: parser extracts a PersonalEvent regardless of classification.

        Zoom automated reminders may classify as 'other'; this test validates
        parsing quality with an explicit domain only.
        """
        results = self._parse("meeting.json", "personal")
        self._assert_schema(
            results,
            PersonalEvent,
            required={"event_name": "Standup"},
            optional={"date": "2026-03-16", "time": "09:00"},
            label="meeting",
        )

    # ── PDF / DOCX documents ─────────────────────────────────────────────────

    def test_document_contract_pdf(self) -> None:
        """Lease email + PDF attachment: email body + converted PDF classifies as legal, extracts Contract."""
        text = self._text_with_attachments("contract_signed_pdf.json")

        s = self.__class__._stats
        s["domains_tested"] += 1
        result = self.pipeline.domain_classifier(text)
        domain, confidence = result["domain"], result["confidence"]
        if domain == "legal":
            s["domains_correct"] += 1
        self.assertEqual(
            domain,
            "legal",
            f"Expected 'legal' for lease email+PDF, got='{domain}' (confidence={confidence:.2f})",
        )

        results = self.pipeline.domain_parser(text, "legal")
        self._assert_schema(
            results,
            Contract,
            required={"title": "Lease Agreement"},
            optional={
                "effective_date": "2026-06-01",
                "expiry_date": "2027-05-31",
                "description": "residential",
            },
            label="contract_signed_pdf",
        )

    def test_document_medical_report_docx(self) -> None:
        """Lab results email + DOCX attachment: email body + converted DOCX classifies as health, extracts MedicalHistory."""
        text = self._text_with_attachments("medical_report_docx.json")

        s = self.__class__._stats
        s["domains_tested"] += 1
        result = self.pipeline.domain_classifier(text)
        domain, confidence = result["domain"], result["confidence"]
        if domain == "health":
            s["domains_correct"] += 1
        self.assertEqual(
            domain,
            "health",
            f"Expected 'health' for lab results email+DOCX, got='{domain}' (confidence={confidence:.2f})",
        )

        results = self.pipeline.domain_parser(text, "health")
        self._assert_schema(
            results,
            MedicalHistory,
            required={"disease": "Hypercholesterolemia", "date": "2026"},
            optional={"description": "cholesterol"},
            label="medical_report_docx",
        )

    # ── out-of-domain ─────────────────────────────────────────────────────────

    def _assert_no_entries(self, scenario_file: str) -> None:
        """Run the full pipeline and assert it returns no entries."""
        s = self.__class__._stats
        s["domains_tested"] += 1
        data = self._load(scenario_file)
        results = self.pipeline(self._text(data))
        if not results:
            s["domains_correct"] += 1
        self.assertEqual(
            results,
            [],
            f"[{scenario_file}] expected no entries from pipeline, "
            f"got {[type(r).__name__ for r in results]}",
        )

    def test_out_of_domain_shipping(self) -> None:
        """Amazon shipping notification: pipeline returns no entries."""
        self._assert_no_entries("shipping.json")

    def test_out_of_domain_password_reset(self) -> None:
        """GitHub password reset email: pipeline returns no entries."""
        self._assert_no_entries("password_reset.json")

    def test_out_of_domain_marketing(self) -> None:
        """Promotional/marketing email: pipeline returns no entries."""
        self._assert_no_entries("marketing.json")


if __name__ == "__main__":
    import unittest

    unittest.main()
