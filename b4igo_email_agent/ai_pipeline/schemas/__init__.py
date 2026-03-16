"""Subpackage containing schemas and related utilities."""

from b4igo_email_agent.ai_pipeline.schemas.legal_schemas import (
    Attorney,
    Contract,
    CourtDate,
    LegalNotice,
)
from b4igo_email_agent.ai_pipeline.schemas.personal_schemas import (
    Contact,
    PersonalEvent,
    Reminder,
)
from b4igo_email_agent.ai_pipeline.schemas.schemas import (
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
