"""Vault client and backend selection for vault CRUD operations."""

import os
from typing import Any, Optional, Protocol, Union

from shared.schemas.health_schemas import Doctor, Insurance, MedicalHistory, Medication
from shared.vault.b4igo_api_storage import B4igoVaultApiStorage
from shared.vault.storage import VaultStorage

VaultRecord = Union[Doctor, Insurance, Medication, MedicalHistory]

_SCHEMA_TO_TYPE = {
    "Doctor": "doctor",
    "Insurance": "insurance",
    "Medication": "medication",
    "MedicalHistory": "medical_history",
}


class VaultStorageLike(Protocol):
    """Storage contract used by VaultClient."""

    def add_record(
        self, username: str, record_type: str, payload: dict[str, Any]
    ) -> Optional[int]:
        """Create record."""

    def get_records(
        self,
        username: str,
        record_type: Optional[str] = None,
        id: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Read records."""

    def update_record(
        self,
        id: int,
        payload: dict[str, Any],
        record_type: str = "",
        username: str = "",
    ) -> bool:
        """Update record."""

    def delete_record(self, id: int, record_type: str = "", username: str = "") -> bool:
        """Delete record."""


def build_vault_storage_from_env() -> VaultStorageLike:
    """Select vault backend using environment configuration.

    Backends:
    - api: Uses B4igoVaultApiStorage
    - sqlite/local/default: Uses VaultStorage
    """
    backend = os.environ.get("B4IGO_VAULT_BACKEND", "").strip().lower()
    if backend == "api":
        base_url = os.environ.get("B4IGO_API_BASE_URL", "").strip()
        if base_url:
            return B4igoVaultApiStorage(base_url=base_url)
    return VaultStorage()


class VaultClient:
    """Vault CRUD client validated by schema types."""

    def __init__(self, storage: Optional[VaultStorageLike] = None):
        """Initialize with injected storage or env-selected backend."""
        self._storage: VaultStorageLike = storage or build_vault_storage_from_env()

    def _record_type(self, record: VaultRecord) -> str:
        """Map schema class to storage record_type."""
        return _SCHEMA_TO_TYPE.get(type(record).__name__, "")

    def create(self, username: str, record: VaultRecord) -> Optional[int]:
        """Create a vault record for a user."""
        record_type = self._record_type(record)
        if not record_type:
            return None
        return self._storage.add_record(username, record_type, record.model_dump())

    def read(
        self,
        username: str,
        record_type: Optional[str] = None,
        id: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Read vault records."""
        return self._storage.get_records(
            username=username, record_type=record_type, id=id
        )

    def update(self, id: int, record: VaultRecord, username: str = "") -> bool:
        """Update a vault record by id."""
        return self._storage.update_record(
            id, record.model_dump(), self._record_type(record), username
        )

    def delete(self, id: int, record_type: str = "", username: str = "") -> bool:
        """Delete a vault record by id."""
        return self._storage.delete_record(id, record_type, username)
