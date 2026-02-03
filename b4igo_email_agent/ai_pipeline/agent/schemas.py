"""Pydantic models for vault add result and vault schemas."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class VaultAddResult(BaseModel):
    """Result of adding parsed email data to a vault.

    Caller provides vault_type (classification already done). Data is the
    serializable parsed-email payload to add. Persistence is out of scope.
    """

    vault_type: str
    data: Dict[str, Any] = Field(
        description="Parsed email payload (from, to, subject, body, received_at, etc.)"
    )
    errors: List[str] = Field(default_factory=list)
    processing_time_s: Optional[float] = Field(
        default=None, description="Processing time in seconds"
    )


# Vault-type schemas kept for future use (e.g. per-vault validation of data).
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

    appointments: Optional[List[ExtractedAppointment]] = Field(
        default_factory=list,
        description="Medical appointments, consultations, or scheduled visits",
    )
    test_results: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Lab results, test reports, diagnostic results",
    )
    prescriptions: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Prescriptions, medications, or pharmacy information",
    )
    providers: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Healthcare providers, doctors, specialists, or medical facilities",
    )
    insurance: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Insurance claims, coverage information, or policy details",
    )
    medical_records: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Medical records, reports, or documents referenced in email",
    )
    bills: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Medical bills, invoices, or payment information",
    )
    conditions: Optional[List[str]] = Field(
        default_factory=list,
        description="Health conditions, diagnoses, or medical issues mentioned",
    )
    notes: Optional[str] = Field(
        default=None, description="Additional healthcare-related notes or information"
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
