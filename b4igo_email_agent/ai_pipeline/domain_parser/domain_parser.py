"""Defines DomainParser for AI pipeline."""

import json
from pathlib import Path

from ollama import ChatResponse, chat
from pydantic import BaseModel

from b4igo_email_agent.ai_pipeline.domain_classifier import Domain
from b4igo_email_agent.ai_pipeline.schemas import schemas
from b4igo_email_agent.ai_pipeline.schemas.schema_prompter import SchemaPrompter
from b4igo_email_agent.email.models import EmailInput


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

    def _validate_response(self, response_content: str) -> list[BaseModel]:
        """Validates the response content and converts it to BaseModels."""
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
        for result in results:
            schema_name = list(result.keys())[0]

        parsed_results: list[BaseModel] = []
        try:
            for result in results:
                schema_name = list(result.keys())[0]
                schema_fields = result[schema_name]
                schema_class = getattr(schemas, schema_name)
                parsed_result = schema_class(**schema_fields)
                parsed_results.append(parsed_result)
        except Exception as e:
            raise ValueError(f"Error converting JSON to BaseModel instances: {e}")

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
        self.messages.append({"role": "user", "content": schemas_prompt})
        text_email = email.to_text()
        self.messages.append({"role": "user", "content": text_email})

        response: ChatResponse = chat(
            model="qwen3:4b", messages=self.messages, think=False, format="json"
        )
        response_content = response["choices"][0]["message"]["content"]

        entries = self._validate_response(response_content)

        return entries
