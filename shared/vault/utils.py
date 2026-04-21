"""Vault helpers: payload-to-schema mapping for confirmation JSON."""

from typing import Any, Optional, Union

from pydantic import ValidationError

from shared.schemas.schemas import (
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)

VaultRecord = Union[Doctor, Insurance, Medication, MedicalHistory]


def parse_vault_record(payload: Optional[dict[str, Any]]) -> Optional[VaultRecord]:
    """Map a confirmation payload dict to a supported vault schema instance.

    Args:
        payload: Raw dict from jsonPayload, or None.

    Returns:
        Doctor/Insurance/Medication/MedicalHistory instance, or None.
    """
    if not payload or not isinstance(payload, dict):
        return None

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

    return None
