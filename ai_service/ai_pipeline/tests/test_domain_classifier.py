"""Unit tests for DomainClassifier.

These exercise the real sentence-transformers model and a live Ollama server,
so they are gated behind RUN_OLLAMA_TESTS=1 to keep `pytest` and CI from
hanging when no model server is available.
"""

import os
from datetime import datetime
from unittest import TestCase, skipUnless

from ai_service.ai_pipeline.domain_classifier import DomainClassifier
from shared.mail.models import EmailAddress, EmailInput


def _build_email(sender: str, subject: str, body: str) -> EmailInput:
    return EmailInput(
        from_address=EmailAddress(address=sender),
        to_address=[EmailAddress(address="recipient@example.com")],
        subject=subject,
        body=body,
        received_at=datetime.now(),
    )


def _sample_emails() -> list[EmailInput]:
    return [
        _build_email(
            "noreply@hospital.com",
            "Your lab results are ready",
            "Dear Patient, Your recent blood test results are now available.",
        ),
        _build_email(
            "registrar@university.edu",
            "Fall 2024 Transcript Available",
            "Your official transcript for Fall 2024 semester is now available.",
        ),
        _build_email(
            "lawyer@lawfirm.com",
            "RE: Property Deed Transfer",
            "I have reviewed the deed for the property at 123 Main Street.",
        ),
    ]


@skipUnless(
    os.environ.get("RUN_OLLAMA_TESTS") == "1",
    "requires a live Ollama server; set RUN_OLLAMA_TESTS=1 to run",
)
class TestDomainClassifier(TestCase):
    """Unit tests for DomainClassifier classification."""

    emails: list[EmailInput]
    classifier: DomainClassifier

    @classmethod
    def setUpClass(cls) -> None:
        cls.classifier = DomainClassifier()
        cls.emails = _sample_emails()

    def test_classify_returns_results_for_each_email(self) -> None:
        """Ensure each input email returns a result."""
        results = [self.classifier(email.to_text()) for email in self.emails]

        self.assertEqual(len(results), len(self.emails))

    def test_classify_scores_are_well_formed(self) -> None:
        """Validate scores include all categories and a max confidence."""
        results = [self.classifier(email.to_text()) for email in self.emails]

        for result in results:
            self.assertIn(result["domain"], self.classifier._category_list)
            self.assertIsInstance(result["confidence"], float)
            self.assertEqual(
                set(result["all_scores"]),
                set(self.classifier._category_list),
            )
            self.assertEqual(
                result["confidence"],
                max(result["all_scores"].values()),
            )

    def test_classify_empty_string_returns_result(self) -> None:
        """Ensure empty text still returns a classification result."""
        result = self.classifier("")
        self.assertIn(result["domain"], self.classifier._category_list)
        self.assertIsInstance(result["confidence"], float)


if __name__ == "__main__":
    import unittest

    unittest.main()
