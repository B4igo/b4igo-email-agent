"""Defines object for running full pipeline given a document."""

import logging
from typing import Optional

from pydantic import BaseModel

from ai_service.ai_pipeline.domain_classifier import DomainClassifier
from ai_service.ai_pipeline.domain_parser import DomainParser

logger = logging.getLogger(__name__)

# Domains for which a parser exists in shared.schemas.schema_prompter.
# Anything else (e.g. "other") cannot be extracted into structured entries
# today and should be skipped rather than crash the pipeline.
SUPPORTED_DOMAINS: frozenset[str] = frozenset(
    {"education", "health", "legal", "personal"}
)


class AIPipeline:
    """Domain classifier plus parser composed into one callable."""

    def __init__(
        self, reranker_model: Optional[str] = None, parser_model: Optional[str] = None
    ) -> None:
        self.domain_classifier = DomainClassifier(reranker_model)
        self.domain_parser = DomainParser(parser_model)

    def __call__(self, text: str) -> list[BaseModel]:
        """Extract all possible B4iGo entries from a given text.

        Assumes that text belongs to one domain only.

        Args:
            text (str): The document to extract from.

        Returns:
            list[BaseModel]: Pydantic models for each entry. Empty list if the
            classified domain is not one we have a parser for.
        """
        # TODO: Validate size less than max tokens
        # Either have to batch or truncate
        classification_result = self.domain_classifier(text)
        domain = classification_result["domain"]
        if domain not in SUPPORTED_DOMAINS:
            logger.info("skipping unsupported domain %s", domain)
            return []
        extracted_entries = self.domain_parser(text, domain)

        return extracted_entries
