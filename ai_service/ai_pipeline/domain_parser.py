"""Defines DomainParser for AI pipeline."""

import json
from pathlib import Path
from typing import Optional

from ollama import ChatResponse, chat
from pydantic import BaseModel, ValidationError

from shared.schemas.domains import DOMAIN_MODULES, Domain
from shared.schemas.schema_prompter import SchemaPrompter


class DomainParser:
    """Parses a document for all information within a given domain."""

    DEFAULT_MODEL = "qwen3:8b"

    def __init__(self, model: Optional[str] = None) -> None:
        """Initializes DomainParser."""
        self._model = model if model else self.DEFAULT_MODEL
        self.messages: list[dict[str, str]] = []
        self.schema_prompter: SchemaPrompter = SchemaPrompter()

        # Load system prompt from file and add to messages
        system_prompt = (Path(__file__).parent / "system_prompt.txt").read_text(
            encoding="utf-8"
        )
        self.messages.append(
            {
                "role": "system",
                "content": system_prompt,
            }
        )

    def _validate_response(
        self, response_content: Optional[str], domain: Domain
    ) -> list[BaseModel]:
        """Validates the response content and converts it to BaseModels."""
        if not response_content:
            raise ValueError("No response content to parse.")
        json_object = None
        try:
            json_object = json.loads(response_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")
        if "results" not in json_object:
            raise ValueError("JSON response does not contain 'results' key.")
        results = json_object["results"]
        if not isinstance(results, list):
            raise ValueError("'results' key must be a list.")

        module = DOMAIN_MODULES.get(domain)
        parsed_results: list[BaseModel] = []
        for result in results:
            if not isinstance(result, dict) or not result:
                continue
            try:
                schema_name = list(result.keys())[0]
                schema_fields = result[schema_name]
                if module is None:
                    continue
                schema_class = getattr(module, schema_name, None)
                if schema_class is None:
                    continue
                parsed_result = schema_class(**schema_fields)
                parsed_results.append(parsed_result)
            except (ValidationError, IndexError, KeyError, TypeError):
                # Missing keys or invalid fields: skip.
                continue

        return parsed_results

    def __call__(self, text: str, domain: Domain) -> list[BaseModel]:
        """Parses a document for all information within a given domain.

        Args:
            text (str): The document text to be parsed.
            domain (Domain): The domain to parse the document for.

        Returns:
            list[BaseModel]: A list of parsed information as Schema
            instances.
        """
        schemas_prompt = self.schema_prompter.get_domain_prompt(domain)
        # Build messages for this call only so we do not accumulate past documents.
        messages = self.messages + [
            {"role": "user", "content": schemas_prompt},
            {"role": "user", "content": text},
        ]

        response: ChatResponse = chat(
            model=self._model, messages=messages, think=False, format="json"
        )
        response_content = response.message.content
        entries = self._validate_response(response_content, domain)

        return entries
