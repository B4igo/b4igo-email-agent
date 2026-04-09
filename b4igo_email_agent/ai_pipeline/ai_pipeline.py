"""Defines object for running full pipeline given a document."""

from pydantic import BaseModel

from b4igo_email_agent.ai_pipeline.domain_classifier import DomainClassifier
from b4igo_email_agent.ai_pipeline.domain_parser import DomainParser


class AIPipeline:

    def __init__(self) -> None:
        self.domain_classifier = DomainClassifier()
        self.domain_parser = DomainParser()

    def __call__(self, text: str) -> list[BaseModel]:
        """Extract all possible B4iGo entries from a given text.

        Assumes that text belongs to one domain only.

        Args:
            text (str): The document to extract from.

        Returns:
            list[BaseModel]: Pydantic models for each entry.

        """

        # TODO: Validate size less than max tokens
        # Either have to batch or truncate
        classification_result = self.domain_classifier(text)
        extracted_entries = self.domain_parser(text, classification_result["domain"])

        return extracted_entries
