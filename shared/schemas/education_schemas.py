"""Pydantic models for education domain email extraction."""

from typing import Optional

from pydantic import BaseModel, Field


class Education(BaseModel):
    """An educational qualification or enrollment mentioned in an email."""

    institution: str = Field(description="Name of the university, college, or school")
    degree: str = Field(
        description="Degree or certificate name (e.g. Bachelor of Science, MBA)"
    )
    field_of_study: Optional[str] = Field(
        default=None, description="Major, concentration, or field of study"
    )
    start_date: Optional[str] = Field(
        default=None, description="Start date of the program (ISO format)"
    )
    end_date: Optional[str] = Field(
        default=None, description="End or expected graduation date (ISO format)"
    )
    is_currently_pursuing: bool = Field(
        default=False, description="Whether the program is currently in progress"
    )
    gpa: Optional[str] = Field(default=None, description="GPA or academic standing")
    notes: Optional[str] = Field(
        default=None, description="Any additional details about the education record"
    )
