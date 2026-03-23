"""Defines DomainParser for AI pipeline."""

import json
from pathlib import Path
from typing import Optional

from ollama import ChatResponse, chat
from pydantic import BaseModel, ValidationError

import b4igo_email_agent.ai_pipeline.schemas as schemas_pkg
from b4igo_email_agent.ai_pipeline.domain_classifier import Domain
from b4igo_email_agent.ai_pipeline.schemas.schema_prompter import SchemaPrompter
from b4igo_email_agent.mail.models import EmailInput


class DomainParser:
    """Parses email for all information within a given domain."""

    def __init__(self) -> None:
        """Initializes DomainParser."""
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

    def _validate_response(self, response_content: Optional[str]) -> list[BaseModel]:
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

        # TODO - Check for empty strings or null values
        parsed_results: list[BaseModel] = []
        for result in results:
            if not isinstance(result, dict) or not result:
                continue
            try:
                schema_name = list(result.keys())[0]
                schema_fields = result[schema_name]
                schema_class = getattr(schemas_pkg, schema_name)
                parsed_result = schema_class(**schema_fields)
                parsed_results.append(parsed_result)
            except (ValidationError, AttributeError, IndexError, KeyError, TypeError):
                # Invalid schema name, missing keys, or invalid fields: skip.
                continue

        return parsed_results

    def parse_email(self, email: EmailInput, domain: Domain) -> list[BaseModel]:
        """Parses email for all information within a given domain.

        Args:
            email (EmailInput): The email to be parsed.
            domain (Domain): The domain to parse the email for.

        Returns:
            list[BaseModel]: A list of parsed information as Schema
            instances.
        """
        schemas_prompt = self.schema_prompter.get_domain_prompt(domain)
        text_email = email.to_text()
        # Build messages for this call only so we do not accumulate past emails.
        messages = self.messages + [
            {"role": "user", "content": schemas_prompt},
            {"role": "user", "content": text_email},
        ]

        # TODO: Make model configurable
        response: ChatResponse = chat(
            model="qwen3:8b", messages=messages, think=False, format="json"
        )
        response_content = response.message.content
        entries = self._validate_response(response_content)

        return entries
