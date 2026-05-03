"""
AI Pipeline accuracy tests — DomainClassifier + DomainParser end-to-end.

Each test exercises the full pipeline on a realistic natural-language document
and records both classification accuracy and field-level extraction accuracy.

Input documents come in two formats:
  email    — formatted like a typical email (From/Subject/Body)
  document — plain text as if extracted from a PDF or DOCX file

Requires Ollama running locally with the qwen3:8b model pulled.
Tests are intentionally slow; run with -s to see the accuracy report.

Run with:
    python -m pytest ai_service/ai_pipeline/tests/test_ai_pipeline.py -v -s
"""

import unittest
from dataclasses import dataclass
from typing import Optional, Type

from pydantic import BaseModel

from ai_service.ai_pipeline.domain_classifier import DomainClassifier
from ai_service.ai_pipeline.domain_parser import DomainParser
from shared.schemas.legal_schemas import Attorney, Contract, CourtDate, LegalNotice
from shared.schemas.personal_schemas import Contact, PersonalEvent, Reminder
from shared.schemas.schemas import Doctor, Insurance, MedicalHistory, Medication

# Treat a classification as uncertain when confidence falls below this value.
# Adjust this constant based on observed model performance.
CONFIDENCE_THRESHOLD = 0.50


# ---------------------------------------------------------------------------
# Accuracy statistics
# ---------------------------------------------------------------------------


@dataclass
class _AccuracyStats:
    """Module-level tracker for classifier and parser accuracy."""

    classifier_correct: int = 0
    classifier_total: int = 0
    entry_correct: int = 0
    entry_total: int = 0
    field_correct: int = 0
    field_total: int = 0

    def record_classification(self, correct: bool) -> None:
        self.classifier_total += 1
        if correct:
            self.classifier_correct += 1

    def record_entry(self, correct: bool) -> None:
        self.entry_total += 1
        if correct:
            self.entry_correct += 1

    def record_field(self, extracted: bool) -> None:
        self.field_total += 1
        if extracted:
            self.field_correct += 1

    def __str__(self) -> str:
        def pct(n: int, d: int) -> str:
            return f"{100 * n // d}%" if d else "N/A"

        return (
            "\n" + "=" * 60 + "\n"
            "AI Pipeline Accuracy Report\n"
            + "=" * 60 + "\n"
            f"Classifier accuracy : {self.classifier_correct}/{self.classifier_total}"
            f" ({pct(self.classifier_correct, self.classifier_total)})\n"
            f"Entry accuracy      : {self.entry_correct}/{self.entry_total}"
            f" ({pct(self.entry_correct, self.entry_total)})\n"
            f"Field accuracy      : {self.field_correct}/{self.field_total}"
            f" ({pct(self.field_correct, self.field_total)})\n"
            + "=" * 60
        )


_stats = _AccuracyStats()


# ---------------------------------------------------------------------------
# Shared lazy fixtures
# ---------------------------------------------------------------------------

_classifier: Optional[DomainClassifier] = None
_parser: Optional[DomainParser] = None


def _get_classifier() -> DomainClassifier:
    global _classifier
    if _classifier is None:
        _classifier = DomainClassifier()
    return _classifier


def _get_parser() -> DomainParser:
    global _parser
    if _parser is None:
        _parser = DomainParser()
    return _parser


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _check_field(obj: BaseModel, attr: str, substring: Optional[str] = None) -> bool:
    """Return True if attr is non-None and optionally contains substring (case-insensitive)."""
    value = getattr(obj, attr, None)
    if value is None:
        return False
    if substring:
        return substring.lower() in str(value).lower()
    return True


def _first_of(entries: list, schema_cls: Type[BaseModel]) -> Optional[BaseModel]:
    matches = [e for e in entries if isinstance(e, schema_cls)]
    return matches[0] if matches else None


# ---------------------------------------------------------------------------
# Health domain
# ---------------------------------------------------------------------------


class TestHealthPipelineAccuracy(unittest.TestCase):
    """Full-pipeline accuracy for health domain schemas (Doctor, Insurance, Medication, MedicalHistory)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.classifier = _get_classifier()
        cls.parser = _get_parser()

    def _run(self, text: str, schema_cls: Type[BaseModel]) -> Optional[BaseModel]:
        result = self.classifier(text)
        _stats.record_classification(result["domain"] == "health")
        entries = self.parser(text, "health")
        instance = _first_of(entries, schema_cls)
        _stats.record_entry(instance is not None)
        return instance

    def test_doctor_from_email(self) -> None:
        """Classify and parse a doctor-assignment email; check name, specialty, and location."""
        text = (
            "From: admin@greenvalleymedical.com\n"
            "To: patient@example.com\n"
            "Subject: Your New Primary Care Physician — Dr. Patricia Alvarez\n\n"
            "Dear Mr. Thompson,\n\n"
            "We are pleased to inform you that Dr. Patricia Alvarez has been assigned "
            "as your primary care physician, effective March 1, 2026.\n\n"
            "Doctor Name: Dr. Patricia Alvarez\n"
            "Specialty: Family Medicine\n"
            "Practice Location: Green Valley Medical Center, 200 Oak Street, Springfield\n"
            "Date of Assignment: 2026-03-01\n\n"
            "To schedule your first visit, call (555) 234-5678.\n\n"
            "Green Valley Medical Center"
        )
        doctor = self._run(text, Doctor)
        self.assertIsNotNone(doctor, "Parser did not return a Doctor instance")
        assert isinstance(doctor, Doctor)

        self.assertIsNotNone(doctor.doctor_name)
        self.assertIn("Alvarez", doctor.doctor_name)

        for attr, hint in [
            ("type", "family"),
            ("location", "green valley"),
            ("date", "2026"),
        ]:
            _stats.record_field(_check_field(doctor, attr, hint))

    def test_insurance_from_document(self) -> None:
        """Parse insurance details from a plain-text extract of a PDF membership card."""
        text = (
            "HEALTH INSURANCE MEMBERSHIP SUMMARY\n"
            "Extracted from: BlueCross BlueShield Member Card (PDF)\n\n"
            "Plan Type: Blue Cross Blue Shield PPO\n"
            "Coverage Type: Family\n"
            "Member Name: Robert Thompson\n"
            "Member ID: BCB-9876543\n"
            "Group Number: GRP-11223\n"
            "Effective Date: 2026-01-01\n"
            "Renewal Date: 2026-12-31\n\n"
            "Present this card at all healthcare provider visits. "
            "This card confirms coverage under the PPO Family Plan."
        )
        insurance = self._run(text, Insurance)
        self.assertIsNotNone(insurance, "Parser did not return an Insurance instance")
        assert isinstance(insurance, Insurance)

        self.assertIsNotNone(insurance.type_of_health_insurance)
        self.assertIsNotNone(insurance.coverage_type)
        self.assertIn("PPO", insurance.type_of_health_insurance.upper())
        self.assertIn("Family", insurance.coverage_type)

        _stats.record_field(_check_field(insurance, "last_updated", "2026"))

    def test_medication_from_email(self) -> None:
        """Parse medication details from a pharmacy prescription notification email."""
        text = (
            "From: pharmacy@rxplus.com\n"
            "To: chen.alice@example.com\n"
            "Subject: Prescription Ready — Lisinopril 10mg\n\n"
            "Dear Ms. Chen,\n\n"
            "Your prescription is ready for pickup at RxPlus Pharmacy.\n\n"
            "Medication Name: Lisinopril 10mg\n"
            "Treatment Purpose: Blood pressure management\n"
            "Duration: 30-day supply, refillable annually\n"
            "Date Prescribed: 2026-02-15\n\n"
            "Please pick up within 14 days. Questions? Call (555) 567-8901.\n\n"
            "RxPlus Pharmacy"
        )
        medication = self._run(text, Medication)
        self.assertIsNotNone(medication, "Parser did not return a Medication instance")
        assert isinstance(medication, Medication)

        self.assertIsNotNone(medication.name_of_medicine)
        self.assertIn("Lisinopril", medication.name_of_medicine)

        for attr, hint in [
            ("purpose", "blood pressure"),
            ("duration", "30"),
            ("date", "2026"),
        ]:
            _stats.record_field(_check_field(medication, attr, hint))

    def test_medical_history_from_document(self) -> None:
        """Parse a medical history entry from plain-text patient record content (simulated PDF)."""
        text = (
            "PATIENT MEDICAL RECORD SUMMARY\n"
            "Document Type: Medical History Extract (PDF)\n\n"
            "Patient: David Kim\n"
            "Record Date: 2026-01-20\n\n"
            "Condition: Type 2 Diabetes Mellitus\n"
            "Description: Patient presented with elevated blood glucose levels "
            "(HbA1c 8.2%). Metformin 500mg prescribed twice daily. "
            "Dietary counseling and routine monitoring recommended.\n\n"
            "Prepared by: Springfield Family Health Clinic"
        )
        history = self._run(text, MedicalHistory)
        self.assertIsNotNone(history, "Parser did not return a MedicalHistory instance")
        assert isinstance(history, MedicalHistory)

        self.assertIsNotNone(history.disease)
        self.assertIsNotNone(history.date)
        self.assertIn("Diabetes", history.disease)

        _stats.record_field(_check_field(history, "description", "blood glucose"))


# ---------------------------------------------------------------------------
# Legal domain
# ---------------------------------------------------------------------------


class TestLegalPipelineAccuracy(unittest.TestCase):
    """Full-pipeline accuracy for legal domain schemas (Attorney, Contract, CourtDate, LegalNotice)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.classifier = _get_classifier()
        cls.parser = _get_parser()

    def _run(self, text: str, schema_cls: Type[BaseModel]) -> Optional[BaseModel]:
        result = self.classifier(text)
        _stats.record_classification(result["domain"] == "legal")
        entries = self.parser(text, "legal")
        instance = _first_of(entries, schema_cls)
        _stats.record_entry(instance is not None)
        return instance

    def test_attorney_from_email(self) -> None:
        """Parse attorney contact info from a legal representation confirmation email."""
        text = (
            "From: jessica.morgan@morganlaw.com\n"
            "To: williams.family@example.com\n"
            "Subject: Engagement Confirmation — Estate Planning\n\n"
            "Dear Mr. and Mrs. Williams,\n\n"
            "I am pleased to confirm that I will represent you in your estate planning matter.\n\n"
            "Attorney: Jessica Morgan\n"
            "Firm: Morgan & Associates Law Group\n"
            "Specialty: Estate Planning and Trusts\n"
            "Email: jessica.morgan@morganlaw.com\n"
            "Phone: (555) 345-6789\n\n"
            "Please review and sign the attached engagement letter at your earliest convenience.\n\n"
            "Jessica Morgan, Esq.\n"
            "Morgan & Associates Law Group"
        )
        attorney = self._run(text, Attorney)
        self.assertIsNotNone(attorney, "Parser did not return an Attorney instance")
        assert isinstance(attorney, Attorney)

        self.assertIsNotNone(attorney.name)
        self.assertIn("Morgan", attorney.name)

        for attr, hint in [
            ("firm", "morgan"),
            ("specialty", "estate"),
            ("email", "@"),
            ("phone", "555"),
        ]:
            _stats.record_field(_check_field(attorney, attr, hint))

    def test_contract_from_document(self) -> None:
        """Parse a contract record from plain-text DOCX content."""
        text = (
            "SERVICE AGREEMENT\n"
            "Document Type: Signed Contract (DOCX Extract)\n\n"
            "Agreement Title: Software Development Services Agreement\n"
            "Parties: TechBuild Solutions LLC and Greenfield Consulting Inc.\n"
            "Effective Date: 2026-03-01\n"
            "Expiration Date: 2027-02-28\n\n"
            "This agreement governs software development services provided by "
            "TechBuild Solutions LLC to Greenfield Consulting Inc. over twelve months. "
            "All deliverables are subject to the terms outlined in Exhibit A."
        )
        contract = self._run(text, Contract)
        self.assertIsNotNone(contract, "Parser did not return a Contract instance")
        assert isinstance(contract, Contract)

        self.assertIsNotNone(contract.title)
        self.assertIn("Software", contract.title)

        for attr, hint in [
            ("effective_date", "2026"),
            ("expiry_date", "2027"),
            ("description", "software"),
        ]:
            _stats.record_field(_check_field(contract, attr, hint))

        if contract.parties:
            _stats.record_field(any("TechBuild" in p for p in contract.parties))
        else:
            _stats.record_field(False)

    def test_court_date_from_email(self) -> None:
        """Parse a hearing date and case details from a court notice email."""
        text = (
            "From: clerk@springfieldcounty.gov\n"
            "To: rodriguez.maria@example.com\n"
            "Subject: Notice of Hearing — Case No. 2026-CV-00451\n\n"
            "Dear Ms. Rodriguez,\n\n"
            "You are hereby notified that a hearing has been scheduled in the above matter.\n\n"
            "Case Number: 2026-CV-00451\n"
            "Hearing Date: 2026-04-15\n"
            "Time: 9:00 AM\n"
            "Court: Springfield County Superior Court, Courtroom 4B\n"
            "Case Type: Civil — Breach of Contract\n\n"
            "Failure to appear may result in a default judgment. "
            "Contact the clerk's office at (555) 100-2000 to reschedule.\n\n"
            "Office of the Court Clerk\n"
            "Springfield County Superior Court"
        )
        court_date = self._run(text, CourtDate)
        self.assertIsNotNone(court_date, "Parser did not return a CourtDate instance")
        assert isinstance(court_date, CourtDate)

        self.assertIsNotNone(court_date.date)
        self.assertIn("2026", court_date.date)

        for attr, hint in [
            ("case_number", "2026-CV"),
            ("court", "Springfield"),
            ("case_type", "civil"),
            ("time", "9"),
        ]:
            _stats.record_field(_check_field(court_date, attr, hint))

    def test_legal_notice_from_document(self) -> None:
        """Parse a legal notice from plain-text scanned PDF content."""
        text = (
            "DEMAND LETTER\n"
            "Document Type: Scanned Legal Notice (PDF)\n\n"
            "Notice Type: Demand for Payment\n"
            "Date: 2026-02-28\n"
            "From: Hartwell Property Management LLC\n"
            "To: Tenant at 450 Riverside Drive, Unit 8\n\n"
            "Subject: Overdue Rent — February 2026\n\n"
            "You are hereby notified that your rent of $1,850.00 for February 2026 "
            "remains unpaid. Full payment must be received by 2026-03-10 or legal "
            "proceedings will be initiated without further notice.\n\n"
            "Hartwell Property Management LLC"
        )
        notice = self._run(text, LegalNotice)
        self.assertIsNotNone(notice, "Parser did not return a LegalNotice instance")
        assert isinstance(notice, LegalNotice)

        self.assertIsNotNone(notice.type)

        for attr, hint in [
            ("sender", "Hartwell"),
            ("date", "2026"),
            ("subject", "rent"),
            ("deadline", "2026"),
        ]:
            _stats.record_field(_check_field(notice, attr, hint))


# ---------------------------------------------------------------------------
# Personal domain
# ---------------------------------------------------------------------------


class TestPersonalPipelineAccuracy(unittest.TestCase):
    """Full-pipeline accuracy for personal domain schemas (Contact, PersonalEvent, Reminder)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.classifier = _get_classifier()
        cls.parser = _get_parser()

    def _run(self, text: str, schema_cls: Type[BaseModel]) -> Optional[BaseModel]:
        result = self.classifier(text)
        _stats.record_classification(result["domain"] == "personal")
        entries = self.parser(text, "personal")
        instance = _first_of(entries, schema_cls)
        _stats.record_entry(instance is not None)
        return instance

    def test_contact_from_email(self) -> None:
        """Parse a contact entry from a personal email introducing a new person."""
        text = (
            "From: tom.baker@example.com\n"
            "To: friend@example.com\n"
            "Subject: Introducing My Sister Sarah\n\n"
            "Hey,\n\n"
            "I wanted to introduce you to my sister Sarah Nakamura. "
            "She's moving to your city next month and would love to meet new people!\n\n"
            "Name: Sarah Nakamura\n"
            "Relationship: Sister\n"
            "Email: sarah.nakamura@gmail.com\n"
            "Phone: (555) 789-0123\n\n"
            "Feel free to reach out to her anytime.\n\n"
            "Cheers, Tom"
        )
        contact = self._run(text, Contact)
        self.assertIsNotNone(contact, "Parser did not return a Contact instance")
        assert isinstance(contact, Contact)

        self.assertIsNotNone(contact.name)
        self.assertIn("Nakamura", contact.name)

        for attr, hint in [
            ("relationship", "sister"),
            ("email", "@"),
            ("phone", "555"),
        ]:
            _stats.record_field(_check_field(contact, attr, hint))

    def test_personal_event_from_email(self) -> None:
        """Parse a personal event from a birthday party invitation email."""
        text = (
            "From: emily.johnson@gmail.com\n"
            "To: friends@example.com\n"
            "Subject: You're Invited! — Emily's 30th Birthday Party\n\n"
            "Hey everyone!\n\n"
            "I'm celebrating my 30th birthday and would love for you to join!\n\n"
            "Event: Emily's 30th Birthday Party\n"
            "Type: Birthday\n"
            "Date: 2026-03-22\n"
            "Time: 7:00 PM\n"
            "Location: The Rooftop Lounge, 88 Harbor View Drive, Downtown\n"
            "Attendees: Close friends and family\n\n"
            "RSVP by March 15th. Light food and drinks provided.\n\n"
            "Love, Emily"
        )
        event = self._run(text, PersonalEvent)
        self.assertIsNotNone(event, "Parser did not return a PersonalEvent instance")
        assert isinstance(event, PersonalEvent)

        self.assertIsNotNone(event.event_name)
        self.assertIn("Birthday", event.event_name)

        for attr, hint in [
            ("type", "birthday"),
            ("date", "2026-03-22"),
            ("time", "7"),
            ("location", "rooftop"),
        ]:
            _stats.record_field(_check_field(event, attr, hint))

    def test_reminder_from_email(self) -> None:
        """Parse a reminder task from an automated reminder notification email."""
        text = (
            "From: reminders@taskapp.com\n"
            "To: user@example.com\n"
            "Subject: Reminder: Renew Your Car Registration — Due March 31\n\n"
            "Hi,\n\n"
            "This is a friendly reminder about an upcoming deadline.\n\n"
            "Task: Renew car registration before the expiration deadline\n"
            "Due Date: 2026-03-31\n"
            "Priority: High\n"
            "Category: Errands\n"
            "Notes: Visit the DMV in person or renew online. "
            "Bring proof of insurance and your current registration notice.\n\n"
            "TaskApp Reminders"
        )
        reminder = self._run(text, Reminder)
        self.assertIsNotNone(reminder, "Parser did not return a Reminder instance")
        assert isinstance(reminder, Reminder)

        self.assertIsNotNone(reminder.task)

        for attr, hint in [
            ("due_date", "2026-03-31"),
            ("priority", "high"),
            ("category", "errands"),
            ("notes", "dmv"),
        ]:
            _stats.record_field(_check_field(reminder, attr, hint))


# ---------------------------------------------------------------------------
# Off-domain classification
# ---------------------------------------------------------------------------


class TestOffDomainClassification(unittest.TestCase):
    """
    Tests that content unrelated to any vault domain is either classified as
    'other' or has confidence below CONFIDENCE_THRESHOLD.

    If these tests fail, the CONFIDENCE_THRESHOLD may need to be raised, or
    the classifier's category descriptions may need tuning.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.classifier = _get_classifier()

    def _assert_other_or_low_confidence(self, text: str, description: str) -> None:
        result = self.classifier(text)
        is_other = result["domain"] == "other"
        is_low_confidence = result["confidence"] < CONFIDENCE_THRESHOLD
        self.assertTrue(
            is_other or is_low_confidence,
            f"{description}: expected 'other' domain or confidence < {CONFIDENCE_THRESHOLD}, "
            f"got domain={result['domain']!r}, confidence={result['confidence']:.2f}",
        )

    def test_promotional_email_is_not_vault_domain(self) -> None:
        """A retail promotional email should not be confidently classified as a vault domain."""
        text = (
            "From: deals@shoppingportal.com\n"
            "To: customer@example.com\n"
            "Subject: This Week's Top Deals — Up to 50% Off!\n\n"
            "Shop the latest sales on electronics, clothing, kitchen appliances, and more. "
            "Use code SPRING20 at checkout for an extra 20% off your entire order. "
            "Free standard shipping on orders over $50. Sale ends Sunday at midnight."
        )
        self._assert_other_or_low_confidence(text, "Promotional email")

    def test_weather_report_is_not_vault_domain(self) -> None:
        """A plain weather forecast should not be confidently classified as a vault domain."""
        text = (
            "Weekend Weather Forecast\n\n"
            "Expect partly cloudy skies with a chance of afternoon showers Saturday. "
            "High temperatures will remain in the mid-60s Fahrenheit through Sunday. "
            "A cold front arrives Monday morning bringing up to half an inch of rain. "
            "Gardeners are advised to water plants before the rain arrives."
        )
        self._assert_other_or_low_confidence(text, "Weather report")

    def test_sports_recap_is_not_vault_domain(self) -> None:
        """A sports news article should not be confidently classified as a vault domain."""
        text = (
            "Game Recap: City Rovers vs. Eastside United\n\n"
            "The City Rovers won a dramatic 3-2 match over Eastside United last night. "
            "Striker Marcus Bell scored twice in the second half, including the winning "
            "goal in the 88th minute. Head coach Dana Price praised the team's resilience "
            "after going down 2-1 at halftime. The Rovers now sit third in the standings."
        )
        self._assert_other_or_low_confidence(text, "Sports recap")

    def test_confidence_field_is_always_valid(self) -> None:
        """Classifier must always return a confidence value in [0, 1]."""
        result = self.classifier("Hello, how are you today?")
        self.assertIn("confidence", result)
        self.assertIsInstance(result["confidence"], float)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)

    def test_all_scores_present_for_ambiguous_text(self) -> None:
        """Classifier must return a score for every domain even on ambiguous input."""
        result = self.classifier("The quick brown fox jumps over the lazy dog.")
        expected_domains = {"education", "health", "legal", "personal", "other"}
        self.assertEqual(set(result["all_scores"].keys()), expected_domains)


# ---------------------------------------------------------------------------
# Accuracy summary (class name starts with Z to sort last)
# ---------------------------------------------------------------------------


class TestZAccuracySummary(unittest.TestCase):
    """Prints the accumulated accuracy report after all other tests have run."""

    def test_z_print_accuracy_report(self) -> None:
        """Print full pipeline accuracy statistics. Always passes."""
        print(_stats)
        self.assertGreater(
            _stats.entry_total,
            0,
            "No pipeline tests ran — nothing to report.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
