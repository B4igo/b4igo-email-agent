"""Subpackage containing schemas and related utilities."""

from shared.ai_pipeline.schemas import legal_schemas  # noqa: F401
from shared.ai_pipeline.schemas import personal_schemas  # noqa: F401
from shared.ai_pipeline.schemas import schemas  # noqa: F401
from shared.ai_pipeline.schemas.legal_schemas import (
    Attorney,
    Contract,
    CourtDate,
    LegalNotice,
)
from shared.ai_pipeline.schemas.personal_schemas import (
    Contact,
    PersonalEvent,
    Reminder,
)
from shared.ai_pipeline.schemas.schemas import (
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
