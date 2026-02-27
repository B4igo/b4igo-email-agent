"""Vault module for B4iGO CRUD operations on health records.

Provides VaultStorage (SQLite persistence), VaultClient (Python CRUD interface
using Doctor, Insurance, Medication, MedicalHistory schemas), and
parse_vault_record for mapping confirmation JSON to schema instances.
"""

from b4igo_email_agent.vault.client import VaultClient
from b4igo_email_agent.vault.storage import VAULT_RECORD_TYPES, VaultStorage
from b4igo_email_agent.vault.utils import parse_vault_record

__all__ = [
    "VAULT_RECORD_TYPES",
    "VaultClient",
    "VaultStorage",
    "parse_vault_record",
]
