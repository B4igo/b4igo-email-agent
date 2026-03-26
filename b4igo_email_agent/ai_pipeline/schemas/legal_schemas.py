"""Pydantic models for legal email content."""

from typing import Optional

from pydantic import BaseModel, Field


class Attorney(BaseModel):
    """Extracted attorney information from legal email."""

    name: str = Field(description="Full name of the attorney")
    firm: Optional[str] = Field(default=None, description="Law firm name")
    email: Optional[str] = Field(default=None, description="Contact email")
    phone: Optional[str] = Field(default=None, description="Contact phone number")
    bar_number: Optional[str] = Field(default=None, description="State bar number")
    specialization: Optional[str] = Field(
        default=None, description="Area of legal specialization"
    )


class Contract(BaseModel):
    """Extracted contract information from legal email."""

    title: str = Field(description="Name or title of the contract")
    parties: Optional[str] = Field(
        default=None,
        description="Parties involved (comma-separated or description)",
    )
    effective_date: Optional[str] = Field(
        default=None, description="When the contract takes effect (ISO format)"
    )
    expiration_date: Optional[str] = Field(
        default=None, description="When the contract expires (ISO format)"
    )
    summary: Optional[str] = Field(
        default=None, description="Brief summary of the contract terms"
    )
    status: Optional[str] = Field(
        default=None,
        description="Current status (e.g. pending, active, expired)",
    )


class CourtDate(BaseModel):
    """Extracted court date or hearing information from legal email."""

    date: str = Field(description="Date of the court appearance (ISO format)")
    case_name: Optional[str] = Field(
        default=None, description="Name of the legal case"
    )
    case_number: Optional[str] = Field(default=None, description="Court case number")
    time: Optional[str] = Field(default=None, description="Time of the hearing")
    location: Optional[str] = Field(
        default=None, description="Court name and address"
    )
    judge: Optional[str] = Field(default=None, description="Presiding judge")
    notes: Optional[str] = Field(
        default=None, description="Additional context or instructions"
    )


class LegalNotice(BaseModel):
    """Extracted legal notice information from email."""

    title: str = Field(description="Title or subject of the legal notice")
    sender: Optional[str] = Field(default=None, description="Who sent the notice")
    date: Optional[str] = Field(
        default=None, description="Date of the notice (ISO format)"
    )
    deadline: Optional[str] = Field(
        default=None,
        description="Response or compliance deadline (ISO format)",
    )
    summary: Optional[str] = Field(
        default=None, description="Brief summary of the notice content"
    )
    action_required: Optional[str] = Field(
        default=None, description="What action the recipient must take"
    )
