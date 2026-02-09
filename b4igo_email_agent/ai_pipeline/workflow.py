"""Add parsed email to vault. Caller provides vault_type (classification done)."""

import logging
from typing import TYPE_CHECKING

from .email.email_parser import email_input_to_message
from .email.models import EmailInput

if TYPE_CHECKING:
    from b4igo_email_agent.ai_pipeline.domain_classifier import (
        DomainClassifier,
        EmailClassificationResult,
    )

logger = logging.getLogger(__name__)


def process_email_to_vault(
    email: EmailInput,
    classifier: "DomainClassifier",
) -> "EmailClassificationResult":
    """Classify email and add to vault in one step. Keeps DomainClassifier unchanged.

    Converts EmailInput to EmailMessage via bridge, calls classifier.classify(),
    then add_email_to_vault with the returned category.
    """
    msg = email_input_to_message(email)
    results = classifier.classify([msg])
    classification = results[0]
    return classification
