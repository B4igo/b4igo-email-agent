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


class ExtractedDoctor(BaseModel):
    """Doctor record aligned with website 'My Doctors Records' table."""

    doctor_name: str = Field(description="Full name of the doctor")
    type: Optional[str] = Field(default=None, description="Specialty or category")
    location: Optional[str] = Field(default=None, description="Practice or association location")
    date: Optional[str] = Field(default=None, description="Record date, last visit, or appointment date")
    id: Optional[int] = Field(default=None, description="Serial number / S.No for API use")


class ExtractedInsurance(BaseModel):
    """Insurance record aligned with website 'My Health Insurance Records' table."""

    type_of_health_insurance: str = Field(description="Plan type (e.g. PPO, HMO, EPO)")
    coverage_type: str = Field(description="Scope (e.g. Individual, Family, Dental, Vision)")
    last_updated: Optional[str] = Field(default=None, description="When the record was last updated")
    id: Optional[int] = Field(default=None, description="Serial number / S.No for API use")


class ExtractedMedication(BaseModel):
    """Medication/treatment record aligned with website treatments and medications table."""

    name_of_medicine: str = Field(description="Name of the medication")
    treatment_name: Optional[str] = Field(default=None, description="Associated treatment name")
    purpose: Optional[str] = Field(default=None, description="Reason or objective of treatment/medication")
    duration: Optional[str] = Field(default=None, description="Length of time prescribed or taken")
    date: Optional[str] = Field(default=None, description="Start, prescription, or related date")
    id: Optional[int] = Field(default=None, description="Serial number / S.No for API use")


class ExtractedMedicalHistoryEntry(BaseModel):
    """Medical history or emergency alert record aligned with website tables."""

    date: str = Field(description="Date of the record or event")
    disease: str = Field(description="Condition or disease")
    description: Optional[str] = Field(default=None, description="Additional details")
    id: Optional[int] = Field(default=None, description="Serial number / S.No for API use")


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

    doctors: Optional[List[ExtractedDoctor]] = Field(
        default_factory=list,
        description="Doctors aligned with My Doctors Records table",
    )
    insurance_records: Optional[List[ExtractedInsurance]] = Field(
        default_factory=list,
        description="Health insurance records aligned with website table",
    )
    medications: Optional[List[ExtractedMedication]] = Field(
        default_factory=list,
        description="Medications/treatments aligned with website table",
    )
    medical_history: Optional[List[ExtractedMedicalHistoryEntry]] = Field(
        default_factory=list,
        description="Medical history / emergency alerts aligned with website table",
    )


class ExtractedBill(BaseModel):
    """Extracted bill information for agent output."""

    amount: float
    currency: str = "USD"
    due_date: str  # ISO format string
    vendor: str
    account_number: Optional[str] = None
    invoice_number: Optional[str] = None

