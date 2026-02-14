"""Vault helpers: payload-to-schema mapping for confirmation JSON."""

from typing import Any, Optional, Union

from pydantic import ValidationError

from b4igo_email_agent.ai_pipeline.schemas.schemas import (
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)

VaultRecord = Union[Doctor, Insurance, Medication, MedicalHistory]


def parse_vault_record(payload: dict[str, Any]) -> Optional[VaultRecord]:
    """Map a confirmation jsonPayload dict to a vault schema instance.

    Identifies schema by distinctive keys, validates, and returns the model.
    Returns None if payload does not match any schema or validation fails.

    Args:
        payload: Raw dict (e.g. from jsonPayload).

    Returns:
        Doctor, Insurance, Medication, or MedicalHistory instance, or None.
    """
    if not payload or not isinstance(payload, dict):
        return None
    # Distinctive keys per schema
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
