"""Pydantic models for legal domain email extraction."""

from typing import List, Optional

from pydantic import BaseModel, Field


class Attorney(BaseModel):
    """A lawyer or legal representative mentioned in an email."""

    name: str = Field(description="Full name of the attorney or lawyer")
    firm: Optional[str] = Field(
        default=None, description="Law firm or organization name"
    )
    specialty: Optional[str] = Field(
        default=None,
        description="Area of legal specialty (e.g. contract law, litigation)",
    )
    email: Optional[str] = Field(default=None, description="Attorney's email address")
    phone: Optional[str] = Field(default=None, description="Attorney's phone number")


class Contract(BaseModel):
    """A contract or legal agreement referenced in an email."""

    title: str = Field(description="Name or title of the contract or agreement")
    parties: Optional[List[str]] = Field(
        default=None, description="Names of the parties involved in the contract"
    )
    effective_date: Optional[str] = Field(
        default=None, description="Date the contract takes effect (ISO format)"
    )
    expiry_date: Optional[str] = Field(
        default=None,
        description="Date the contract expires or deadline for signing (ISO format)",
    )
    description: Optional[str] = Field(
        default=None,
        description="Brief summary of the contract's purpose or subject matter",
    )


class CourtDate(BaseModel):
    """A court hearing, deadline, or legal proceeding date."""

    date: str = Field(description="Date of the court event (ISO format)")
    time: Optional[str] = Field(
        default=None, description="Time of the hearing or proceeding"
    )
    case_number: Optional[str] = Field(
        default=None, description="Case or docket number"
    )
    court: Optional[str] = Field(
        default=None, description="Name or location of the court"
    )
    case_type: Optional[str] = Field(
        default=None, description="Type of case (e.g. civil, criminal, family)"
    )
    notes: Optional[str] = Field(
        default=None, description="Additional notes or instructions"
    )


class LegalNotice(BaseModel):
    """A formal legal notice or regulatory communication."""

    type: str = Field(
        description=(
            "Type of notice (e.g. demand letter, cease and desist, compliance notice)"
        )
    )
    sender: Optional[str] = Field(
        default=None, description="Individual or organization sending the notice"
    )
    date: Optional[str] = Field(
        default=None, description="Date the notice was issued (ISO format)"
    )
    subject: Optional[str] = Field(
        default=None, description="Subject or matter of the notice"
    )
    deadline: Optional[str] = Field(
        default=None, description="Response or compliance deadline (ISO format)"
    )
