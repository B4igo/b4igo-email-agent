"""Subpackage containing schemas and related utilities."""

from .legal_schemas import Attorney, Contract, CourtDate, LegalNotice  # noqa: F401
from .personal_schemas import Contact, PersonalEvent, Reminder  # noqa: F401
from .schemas import (  # noqa: F401
    Appointment,
    Bill,
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)
