"""Add parsed email to vault. Caller provides vault_type (classification done)."""

import logging
import time
from typing import Any, Dict, List

from src.agent.schemas import VaultAddResult
from src.email.models import EmailInput

logger = logging.getLogger(__name__)


def _email_to_vault_data(email: EmailInput) -> Dict[str, Any]:
    """Build a JSON-serializable dict from parsed email for vault storage."""
    from_addr = email.from_address
    from_dict: Dict[str, Any] = (
        from_addr.model_dump()
        if hasattr(from_addr, "model_dump")
        else {"address": str(from_addr), "name": None}
    )
    to_list = [
        (
            addr.model_dump()
            if hasattr(addr, "model_dump")
            else {"address": str(addr), "name": None}
        )
        for addr in email.to_address
    ]
    cc_list = [
        (
            addr.model_dump()
            if hasattr(addr, "model_dump")
            else {"address": str(addr), "name": None}
        )
        for addr in email.cc
    ]
    bcc_list = [
        (
            addr.model_dump()
            if hasattr(addr, "model_dump")
            else {"address": str(addr), "name": None}
        )
        for addr in email.bcc
    ]
    received_at = (
        email.received_at.isoformat()
        if hasattr(email.received_at, "isoformat")
        else str(email.received_at)
    )
    data: Dict[str, Any] = {
        "from_address": from_dict,
        "to_address": to_list,
        "subject": email.subject,
        "body": email.body,
        "received_at": received_at,
        "cc": cc_list,
        "bcc": bcc_list,
    }
    if email.metadata is not None:
        data["metadata"] = (
            email.metadata.model_dump()
            if hasattr(email.metadata, "model_dump")
            else email.metadata
        )
    if email.attachments:
        data["attachments"] = email.attachments
    return data


def add_email_to_vault(email: EmailInput, vault_type: str) -> VaultAddResult:
    """Add parsed email to vault. Caller provides vault_type (classification done).

    Persistence of vault entries is out of scope; returns the payload to add.
    """
    start = time.perf_counter()
    errors: List[str] = []
    try:
        data = _email_to_vault_data(email)
        elapsed = time.perf_counter() - start
        logger.debug(
            "Built vault payload for vault_type=%s in %.3fs", vault_type, elapsed
        )
        return VaultAddResult(
            vault_type=vault_type,
            data=data,
            errors=errors,
            processing_time_s=elapsed,
        )
    except Exception as e:
        logger.exception("Failed to build vault payload")
        errors.append(str(e))
        elapsed = time.perf_counter() - start
        return VaultAddResult(
            vault_type=vault_type,
            data={},
            errors=errors,
            processing_time_s=elapsed,
        )
