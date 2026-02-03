"""Add parsed email to vault. Caller provides vault_type (classification done)."""

import logging
import time
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from .schemas import VaultAddResult
from ..email.models import EmailInput, EmailMetadata
from ..email.email_parser import email_input_to_message

from b4igo_email_agent.ai_pipeline.domain_classifier import (
        DomainClassifier,
        EmailClassificationResult,
    )

if TYPE_CHECKING:
    from b4igo_email_agent.ai_pipeline.domain_classifier import (
        DomainClassifier,
        EmailClassificationResult,
    )

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
            if isinstance(email.metadata, EmailMetadata)
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


def process_email_to_vault(
    email: EmailInput,
    classifier: "DomainClassifier",
) -> Tuple["EmailClassificationResult", VaultAddResult]:
    """Classify email and add to vault in one step. Keeps DomainClassifier unchanged.

    Converts EmailInput to EmailMessage via bridge, calls classifier.classify(),
    then add_email_to_vault with the returned category.
    """


    msg = email_input_to_message(email)
    results = classifier.classify([msg])
    classification = results[0]
    vault_result = add_email_to_vault(email, classification["category"])
    return classification, vault_result
