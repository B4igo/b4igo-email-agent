"""Pydantic models for vault add result and vault schemas."""

from typing import Optional

from pydantic import BaseModel, Field


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
    location: Optional[str] = Field(
        default=None, description="Practice or association location"
    )
    date: Optional[str] = Field(
        default=None, description="Record date, last visit, or appointment date"
    )
    id: Optional[int] = Field(
        default=None, description="Serial number / S.No for API use"
    )


class ExtractedInsurance(BaseModel):
    """Insurance record aligned with website 'My Health Insurance Records' table."""

    type_of_health_insurance: str = Field(description="Plan type (e.g. PPO, HMO, EPO)")
    coverage_type: str = Field(
        description="Scope (e.g. Individual, Family, Dental, Vision)"
    )
    last_updated: Optional[str] = Field(
        default=None, description="When the record was last updated"
    )
    id: Optional[int] = Field(
        default=None, description="Serial number / S.No for API use"
    )


class ExtractedMedication(BaseModel):
    """Medication/treatment record aligned with website treatments and
    medications table."""

    name_of_medicine: str = Field(description="Name of the medication")
    treatment_name: Optional[str] = Field(
        default=None, description="Associated treatment name"
    )
    purpose: Optional[str] = Field(
        default=None, description="Reason or objective of treatment/medication"
    )
    duration: Optional[str] = Field(
        default=None, description="Length of time prescribed or taken"
    )
    date: Optional[str] = Field(
        default=None, description="Start, prescription, or related date"
    )
    id: Optional[int] = Field(
        default=None, description="Serial number / S.No for API use"
    )


class ExtractedMedicalHistoryEntry(BaseModel):
    """Medical history or emergency alert record aligned with website tables."""

    date: str = Field(description="Date of the record or event")
    disease: str = Field(description="Condition or disease")
    description: Optional[str] = Field(default=None, description="Additional details")
    id: Optional[int] = Field(
        default=None, description="Serial number / S.No for API use"
    )


class ExtractedBill(BaseModel):
    """Extracted bill information for agent output."""

    amount: float
    currency: str = "USD"
    due_date: str  # ISO format string
    vendor: str
    account_number: Optional[str] = None
    invoice_number: Optional[str] = None
