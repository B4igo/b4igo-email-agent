"""Pydantic models for personal email content."""

from typing import Optional

from pydantic import BaseModel, Field


class Contact(BaseModel):
    """Extracted contact information from personal email."""

    name: str = Field(description="Full name of the contact")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    relationship: Optional[str] = Field(
        default=None,
        description="Relationship to the user (e.g. friend, family, colleague)",
    )
    notes: Optional[str] = Field(default=None, description="Any additional notes")


class PersonalEvent(BaseModel):
    """Extracted personal event or gathering from email."""

    title: str = Field(description="Title or name of the event")
    date: str = Field(description="Date of the event in ISO format")
    time: Optional[str] = Field(default=None, description="Time of the event")
    location: Optional[str] = Field(
        default=None, description="Where the event takes place"
    )
    attendees: Optional[str] = Field(
        default=None,
        description="Who is attending (comma-separated or description)",
    )
    notes: Optional[str] = Field(default=None, description="Additional details")


class Reminder(BaseModel):
    """Extracted reminder or task from personal email."""

    title: str = Field(description="What to be reminded about")
    due_date: Optional[str] = Field(
        default=None, description="When the reminder is due (ISO format)"
    )
    priority: Optional[str] = Field(
        default=None, description="Priority level (e.g. high, medium, low)"
    )
    notes: Optional[str] = Field(default=None, description="Additional context")
