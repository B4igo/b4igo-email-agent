#!/usr/bin/env python3
"""Test script for the email workflow."""
from datetime import datetime

import requests

from b4igo_email_agent.ai_pipeline.domain_classifier import DomainClassifier
from b4igo_email_agent.ai_pipeline.domain_parser import DomainParser
from b4igo_email_agent.email.models import EmailAddress, EmailInput

email = EmailInput(
    from_address=EmailAddress(
        address="appointments@cityhospital.com", name="City Hospital Scheduling"
    ),
    to_address=[EmailAddress(address="patient@email.com", name="John Doe")],
    subject="Appointment Confirmation - Dr. Sarah Johnson",
    body="""Dear John Doe, This email confirms your upcoming appointment
         on March 15, 2026 at 10:30 AM with Dr. Sarah Johnson
         (Cardiologist) at City Hospital, 123 Medical Plaza, Suite 400.
         This is a follow-up consultation that will last approximately
         30 minutes. Please arrive 15 minutes early to complete any
         necessary paperwork. Best regards, City Hospital""",
    received_at=datetime.fromisoformat("2026-02-09T10:30:00"),
)
domain_classifer = DomainClassifier()
domain_parser = DomainParser()


classification_result = domain_classifer.classify([email])[0]
parsed_models = domain_parser.parse_email(email, classification_result["category"])
print(parsed_models)

# API Call
url = "http://localhost:5000/api/confirmations/enqueue"

for parsed_model in parsed_models:
    payload = {"username": "user", "jsonPayload": parsed_model.model_dump_json()}

    response = requests.post(url, json=payload)
    print(response)
