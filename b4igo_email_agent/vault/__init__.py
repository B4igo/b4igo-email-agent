"""Vault module for local or B4iGO-backed CRUD operations."""

from b4igo_email_agent.vault.b4igo_api_storage import B4igoVaultApiStorage
from b4igo_email_agent.vault.client import VaultClient, build_vault_storage_from_env
from b4igo_email_agent.vault.storage import VAULT_RECORD_TYPES, VaultStorage
from b4igo_email_agent.vault.utils import parse_vault_record

__all__ = [
    "B4igoVaultApiStorage",
    "VAULT_RECORD_TYPES",
    "VaultClient",
    "VaultStorage",
    "build_vault_storage_from_env",
    "parse_vault_record",
]
