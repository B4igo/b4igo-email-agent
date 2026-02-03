#!/usr/bin/env python3
"""Demo script for the agent workflow: parse -> classify -> vault.

Run from repo root with venv activated and deps installed:
    pip install numpy sentence-transformers scikit-learn pydantic
    python -m b4igo_email_agent.ai_pipeline.tests.demo_agent_workflow

Or from anywhere (script adds repo root to PYTHONPATH):
    python b4igo_email_agent/ai_pipeline/tests/demo_agent_workflow.py
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path so b4igo_email_agent is importable when run as script
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from datetime import datetime


def main() -> None:
    from b4igo_email_agent.ai_pipeline.agent.workflow import process_email_to_vault
    from b4igo_email_agent.ai_pipeline.domain_classifier import DomainClassifier
    from b4igo_email_agent.ai_pipeline.email.email_parser import parse_email
    from b4igo_email_agent.ai_pipeline.email.models import EmailAddress, EmailInput

    print("=" * 60)
    print("Agent workflow demo: email -> classify -> vault")
    print("=" * 60)

    # Sample emails as JSON (parse_email path) and as EmailInput (direct path)
    samples = [
        {
            "from_address": "noreply@hospital.com",
            "to_address": ["patient@example.com"],
            "subject": "Your lab results are ready",
            "body": "Dear Patient, Your recent blood test results are now available in the patient portal.",
            "received_at": datetime.now().isoformat(),
        },
        {
            "from_address": "registrar@university.edu",
            "to_address": ["student@example.com"],
            "subject": "Fall 2024 Transcript Available",
            "body": "Your official transcript for Fall 2024 semester is now available for download.",
            "received_at": datetime.now().isoformat(),
        },
        {
            "from_address": "lawyer@lawfirm.com",
            "to_address": ["client@example.com"],
            "subject": "RE: Property Deed Transfer",
            "body": "I have reviewed the deed for the property at 123 Main Street. Please sign and return by Friday.",
            "received_at": datetime.now().isoformat(),
        },
    ]

    print("\nLoading classifier (first run may download the model)...")
    classifier = DomainClassifier()
    print("Classifier ready.\n")

    for i, data in enumerate(samples, 1):
        print(f"--- Email {i}: {data['subject'][:50]}...")
        email = parse_email(data)
        classification, vault_result = process_email_to_vault(email, classifier)
        print(f"  Category:   {classification['category']}")
        print(f"  Confidence: {classification['confidence']:.3f}")
        print(f"  Vault type: {vault_result.vault_type}")
        print(f"  Vault OK:   {len(vault_result.errors) == 0} (errors: {vault_result.errors})")
        print(f"  Payload:    {len(vault_result.data)} keys (from_address, to_address, subject, body, ...)")
        print()

    print("=" * 60)
    print("Done. Processed", len(samples), "emails through the agent workflow.")
    print("=" * 60)


if __name__ == "__main__":
    main()
