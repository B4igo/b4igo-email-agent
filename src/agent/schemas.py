"""Pydantic models for agent output and structured responses."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ExtractedAppointment(BaseModel):
    """Extracted appointment information for agent output."""

    date: str  # ISO format string
    time: Optional[str] = None
    provider: str
    location: Optional[str] = None
    appointment_type: Optional[str] = None
    duration: Optional[int] = None
    notes: Optional[str] = None


class HealthcareVaultSchema(BaseModel):
    """Schema for healthcare vault data extracted from emails."""

    # Appointments
    appointments: Optional[List[ExtractedAppointment]] = Field(
        default_factory=list,
        description="Medical appointments, consultations, or scheduled visits"
    )

    # Test results and lab reports
    test_results: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Lab results, test reports, diagnostic results"
    )

    # Prescriptions and medications
    prescriptions: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Prescriptions, medications, or pharmacy information"
    )

    # Medical providers
    providers: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Healthcare providers, doctors, specialists, or medical facilities"
    )

    # Insurance information
    insurance: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Insurance claims, coverage information, or policy details"
    )

    # Medical records or documents
    medical_records: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Medical records, reports, or documents referenced in email"
    )

    # Billing and payments
    bills: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Medical bills, invoices, or payment information"
    )

    # Health conditions or diagnoses
    conditions: Optional[List[str]] = Field(
        default_factory=list,
        description="Health conditions, diagnoses, or medical issues mentioned"
    )

    # Other healthcare-related information
    notes: Optional[str] = Field(
        default=None,
        description="Additional healthcare-related notes or information"
    )


class ExtractedBill(BaseModel):
    """Extracted bill information for agent output."""

    amount: float
    currency: str = "USD"
    due_date: str  # ISO format string
    vendor: str
    account_number: Optional[str] = None
    invoice_number: Optional[str] = None
    service_period: Optional[str] = None


class SuggestedAction(BaseModel):
    """Suggested action from agent."""

    action_type: str  # e.g., "calendar", "reminder", "update_contact"
    description: str
    params: Dict[str, Any] = Field(default_factory=dict)
    priority: Optional[str] = None  # "high", "medium", "low"
    due_date: Optional[str] = None  # ISO format string


class VaultExtraction(BaseModel):
    """Structured output from agent for vault extraction."""

    vault_type: str  # One of 8 vault types: personal_info, healthcare, digital_accounts,
                     # key_master_directives, legal, comms, end_of_life, financial
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score for vault categorization")
    extracted_data: Dict[str, Any] = Field(description="Structured extracted data matching vault schema")
    suggested_actions: List[SuggestedAction] = Field(default_factory=list)
    reasoning: Optional[str] = Field(None, description="Agent's reasoning for categorization and extraction")
    multiple_vaults: Optional[List[str]] = Field(None, description="If email belongs to multiple vaults")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "vault_type": "healthcare",
                "confidence": 0.95,
                "extracted_data": {
                    "appointments": [
                        {
                            "date": "2024-01-15T10:00:00",
                            "time": "10:00 AM",
                            "provider": "Dr. Smith",
                            "location": "123 Medical Center"
                        }
                    ]
                },
                "suggested_actions": [
                    {
                        "action_type": "calendar",
                        "description": "Add appointment to calendar",
                        "params": {
                            "title": "Appointment with Dr. Smith",
                            "date": "2024-01-15T10:00:00"
                        }
                    }
                ]
            }
        }


class ClassificationResult(BaseModel):
    """Result from email classification."""

    vault_type: str
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score for classification")
    reasoning: Optional[str] = None
    multiple_vaults: Optional[List[str]] = Field(None, description="If email belongs to multiple vaults")


class AgentPlan(BaseModel):
    """Structured plan for email processing."""

    vault_type: str
    extraction_steps: List[str]
    validation_steps: List[str]
    actions_needed: bool
    suggested_actions: List[str]
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)


class AgentResponse(BaseModel):
    """Complete agent response including metadata."""

    extraction: VaultExtraction
    processing_time: Optional[float] = None  # Seconds
    tools_used: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


def get_vault_schema_definition(vault_type: str) -> str:
    """Get the schema definition for a vault type as a string for LLM prompts."""
    if vault_type == "healthcare":
        return """The healthcare vault schema expects a JSON object with the following structure:

{
  "appointments": [
    {
      "date": "ISO date string (required)",
      "time": "Time string (optional)",
      "provider": "Provider name (required)",
      "location": "Location/address (optional)",
      "appointment_type": "Type of appointment (optional)",
      "duration": "Duration in minutes (optional)",
      "notes": "Additional notes (optional)"
    }
  ],
  "test_results": [
    {
      "test_name": "Name of test",
      "date": "Date of test",
      "results": "Test results or summary",
      "provider": "Provider who ordered test"
    }
  ],
  "prescriptions": [
    {
      "medication": "Medication name",
      "dosage": "Dosage information",
      "prescribing_provider": "Provider name",
      "pharmacy": "Pharmacy information",
      "refill_date": "Refill date if applicable"
    }
  ],
  "providers": [
    {
      "name": "Provider name",
      "specialty": "Medical specialty",
      "contact": "Contact information",
      "facility": "Medical facility or practice"
    }
  ],
  "insurance": {
    "provider": "Insurance company name",
    "policy_number": "Policy number",
    "claim_number": "Claim number if applicable",
    "status": "Claim or coverage status"
  },
  "medical_records": [
    {
      "type": "Type of record",
      "date": "Date of record",
      "provider": "Provider or facility",
      "summary": "Brief summary"
    }
  ],
  "bills": [
    {
      "amount": "Bill amount",
      "due_date": "Due date",
      "provider": "Billing provider",
      "service": "Service description",
      "account_number": "Account number"
    }
  ],
  "conditions": ["List of health conditions or diagnoses mentioned"],
  "notes": "Any additional healthcare-related notes"
}

All fields are optional except where marked as required. Extract only the information that is present in the email."""
    else:
        return f"Extract structured data for the {vault_type} vault. Return a JSON object with relevant fields based on the email content."