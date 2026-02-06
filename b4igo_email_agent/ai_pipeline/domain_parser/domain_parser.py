"""Defines DomainParser for AI pipeline."""
from importlib.resources import files
import json

from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel

from b4igo_email_agent.ai_pipeline.domain_classifier import Domain
from b4igo_email_agent.ai_pipeline.email.models import EmailInput
from b4igo_email_agent.ai_pipeline.agent import schemas
from b4igo_email_agent.ai_pipeline.domain_parser import prompts


class DomainParser():
    """Parses email for all information within a given domain.
    """

    def __init__(self) -> None:
        """Initializes DomainParser."""

        self.messages: list[dict[str, str]] = []

        # Load base system prompt
        system_prompt = self._load_prompt('system')
        self.messages.append({'role': 'system', 'content': system_prompt})

    def _get_domain_prompt(self, domain: Domain) -> str:
        """Loads the relevant schemas.py file as a prompt for the given
        domain."""
        domain_prompt = files(schemas).joinpath(f'{domain}.py').read_text()
        
        # Remove first 5 lines (imports)
        domain_prompt_lines = domain_prompt.splitlines()
        domain_prompt = '\n'.join(domain_prompt_lines[5:])

        return domain_prompt
    
    def _load_prompt(self, name: str, extension: str = "txt") -> str:
        """Load prompt from the current package."""
        return files(prompts).joinpath(f'{name}.{extension}').read_text()

    def _validate_response(self, response_content: str) -> list[BaseModel]:
        """Validates the response content and converts it to a list of
        BaseModel instances."""

        json_object = None
        try:
            json_object = json.loads(response_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")
        if 'results' not in json_object:
            raise ValueError("JSON response does not contain 'results' key.")
        results = json_object['results']
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

        schemas_prompt = self._get_domain_prompt(domain)
        self.messages.append({'role': 'assistant', 'content': schemas_prompt})
        text_email = email.to_text()
        self.messages.append({'role': 'user', 'content': text_email})

        response: ChatResponse = chat(
            model='qwen3:4b',
            messages=self.messages,
            think=False,
            format='json')
        response_content = response['choices'][0]['message']['content']

        entries = self._validate_response(response_content)

        return entries
