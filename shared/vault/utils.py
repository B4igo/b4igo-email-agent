"""Vault helpers: payload-to-schema mapping for confirmation JSON."""

from typing import Any, Optional, Union

from pydantic import ValidationError

from shared.schemas.education_schemas import Education
from shared.schemas.legal_schemas import Attorney, Contract, CourtDate, LegalNotice
from shared.schemas.personal_schemas import Contact, PersonalEvent, Reminder
from shared.schemas.schemas import Doctor, Insurance, MedicalHistory, Medication

VaultRecord = Union[
    Doctor,
    Insurance,
    Medication,
    MedicalHistory,
    Education,
    Attorney,
    Contract,
    CourtDate,
    LegalNotice,
    Contact,
    PersonalEvent,
    Reminder,
]


def parse_vault_record(payload: Optional[dict[str, Any]]) -> Optional[VaultRecord]:
    """Map a confirmation payload dict to a supported vault schema instance.

    Args:
        payload: Raw dict from jsonPayload, or None.

    Returns:
        A vault schema instance, or None if the payload cannot be mapped.
    """
    if not payload or not isinstance(payload, dict):
        return None

    # Health
    if "doctor_name" in payload:
        try:
            return Doctor.model_validate(payload)
        except ValidationError:
            return None

    if "type_of_health_insurance" in payload and "coverage_type" in payload:
        try:
            return Insurance.model_validate(payload)
        except ValidationError:
            return None

    if "name_of_medicine" in payload:
        try:
            return Medication.model_validate(payload)
        except ValidationError:
            return None

    if "disease" in payload and "date" in payload:
        try:
            return MedicalHistory.model_validate(payload)
        except ValidationError:
            return None

    # Education
    if "institution" in payload and "degree" in payload:
        try:
            return Education.model_validate(payload)
        except ValidationError:
            return None

    # Legal
    if "firm" in payload or "specialty" in payload:
        try:
            return Attorney.model_validate(payload)
        except ValidationError:
            return None

    if "title" in payload and "parties" in payload:
        try:
            return Contract.model_validate(payload)
        except ValidationError:
            return None

    if "case_number" in payload or "court" in payload:
        try:
            return CourtDate.model_validate(payload)
        except ValidationError:
            return None

    if "type" in payload and "sender" in payload:
        try:
            return LegalNotice.model_validate(payload)
        except ValidationError:
            return None

    # Personal
    if "event_name" in payload:
        try:
            return PersonalEvent.model_validate(payload)
        except ValidationError:
            return None

    if "task" in payload:
        try:
            return Reminder.model_validate(payload)
        except ValidationError:
            return None

    if "name" in payload and "relationship" in payload:
        try:
            return Contact.model_validate(payload)
        except ValidationError:
            return None

    return None
