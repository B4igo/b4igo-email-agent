"""Vault client: Python interface for vault CRUD using schema models."""

from typing import Any, Optional, Union

from b4igo_email_agent.ai_pipeline.schemas.schemas import (
    Doctor,
    Insurance,
    MedicalHistory,
    Medication,
)
from b4igo_email_agent.vault.storage import VaultStorage

VaultRecord = Union[Doctor, Insurance, Medication, MedicalHistory]

_SCHEMA_TO_TYPE = {
    "Doctor": "doctor",
    "Insurance": "insurance",
    "Medication": "medication",
    "MedicalHistory": "medical_history",
}


class VaultClient:
    """Vault CRUD client. Validates via Pydantic schemas; uses VaultStorage."""

    def __init__(self, storage: Optional[VaultStorage] = None):
        """Initialize client with optional storage (default: new VaultStorage())."""
        self._storage = storage or VaultStorage()

    def _record_type(self, record: VaultRecord) -> str:
        """Map schema class to storage record_type."""
        return _SCHEMA_TO_TYPE.get(type(record).__name__, "")

    def create(self, username: str, record: VaultRecord) -> Optional[int]:
        """Create a vault record for the user.

        Args:
            username: Owner of the record.
            record: Doctor, Insurance, Medication, or MedicalHistory instance.

        Returns:
            New record id, or None if invalid or storage error.
        """
        record_type = self._record_type(record)
        if not record_type:
            return None
        payload = record.model_dump()
        return self._storage.add_record(username, record_type, payload)

    def read(
        self,
        username: str,
        record_type: Optional[str] = None,
        id: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Read vault records for the user.

        Args:
            username: Owner to filter by.
            record_type: Optional filter (doctor, insurance, medication,
                medical_history).
            id: Optional single record id.

        Returns:
            List of dicts with id, username, record_type, payload (parsed).
        """
        return self._storage.get_records(
            username=username,
            record_type=record_type,
            id=id,
        )

    def update(self, id: int, record: VaultRecord) -> bool:
        """Update a vault record by id.

        Args:
            id: Record id.
            record: Doctor, Insurance, Medication, or MedicalHistory instance.

        Returns:
            True if updated, False otherwise.
        """
        payload = record.model_dump()
        return self._storage.update_record(id, payload)

    def delete(self, id: int) -> bool:
        """Delete a vault record by id.

        Args:
            id: Record id.

        Returns:
            True if deleted, False otherwise.
        """
        return self._storage.delete_record(id)
