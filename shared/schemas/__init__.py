"""Subpackage containing schemas and related utilities."""

from shared.schemas.legal_schemas import Attorney, Contract, CourtDate, LegalNotice
from shared.schemas.personal_schemas import Contact, PersonalEvent, Reminder
from shared.schemas.health_schemas import (
    Appointment,
    Bill,
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)

__all__ = [
    "Appointment",
    "Attorney",
    "Bill",
    "Contact",
    "Contract",
    "CourtDate",
    "Doctor",
    "Insurance",
    "LegalNotice",
    "MedicalHistory",
    "Medication",
    "PersonalEvent",
    "Reminder",
]
