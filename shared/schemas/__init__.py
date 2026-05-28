"""Subpackage containing schemas and related utilities."""

from shared.schemas import education_schemas  # noqa: F401
from shared.schemas import legal_schemas  # noqa: F401
from shared.schemas import personal_schemas  # noqa: F401
from shared.schemas import schemas  # noqa: F401
from shared.schemas.education_schemas import Education
from shared.schemas.legal_schemas import Attorney, Contract, CourtDate, LegalNotice
from shared.schemas.personal_schemas import Contact, PersonalEvent, Reminder
from shared.schemas.schemas import (
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
    "Education",
    "Insurance",
    "LegalNotice",
    "MedicalHistory",
    "Medication",
    "PersonalEvent",
    "Reminder",
]
