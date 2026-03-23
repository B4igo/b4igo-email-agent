"""Pydantic models for personal domain email extraction."""

from typing import List, Optional

from pydantic import BaseModel, Field


class Contact(BaseModel):
    """A person mentioned or referenced in a personal email."""

    name: str = Field(description="Full name of the contact")
    relationship: Optional[str] = Field(
        default=None,
        description="Relationship to the recipient (e.g. friend, sibling, colleague)",
    )
    email: Optional[str] = Field(default=None, description="Contact's email address")
    phone: Optional[str] = Field(default=None, description="Contact's phone number")
    notes: Optional[str] = Field(
        default=None, description="Any additional notes about the contact"
    )


class PersonalEvent(BaseModel):
    """A personal event, occasion, or gathering mentioned in an email."""

    event_name: str = Field(description="Name or title of the event")
    type: Optional[str] = Field(
        default=None,
        description="Type of event (e.g. birthday, wedding, reunion, vacation, dinner)",
    )
    date: Optional[str] = Field(
        default=None, description="Date of the event (ISO format)"
    )
    time: Optional[str] = Field(default=None, description="Time of the event")
    location: Optional[str] = Field(
        default=None, description="Location or venue of the event"
    )
    attendees: Optional[List[str]] = Field(
        default=None, description="Names of people attending or invited"
    )
    description: Optional[str] = Field(
        default=None, description="Additional details about the event"
    )


class Reminder(BaseModel):
    """A personal reminder or to-do item mentioned in an email."""

    task: str = Field(description="Description of the task or reminder")
    due_date: Optional[str] = Field(
        default=None, description="Due date or deadline for the task (ISO format)"
    )
    priority: Optional[str] = Field(
        default=None, description="Priority level (e.g. high, medium, low)"
    )
    category: Optional[str] = Field(
        default=None,
        description="Category or tag for the reminder (e.g. family, errands, health)",
    )
    notes: Optional[str] = Field(
        default=None, description="Additional notes or context"
    )
