"""Schema prompt builder for domain-specific extraction."""

from __future__ import annotations

import json
from types import ModuleType
from typing import Type

from pydantic import BaseModel

from ..domain_classifier import Domain
from . import health_schemas


class SchemaPrompter:
    """Builds prompts containing schema JSON for a given domain."""

    _DOMAIN_MODULES: dict[Domain, ModuleType] = {
        "health": health_schemas,
    }

    def get_domain_prompt(self, domain: Domain) -> str:
        """Return a prompt containing JSON schemas for the given
        domain."""

        module = self._DOMAIN_MODULES.get(domain)
        if module is None:
            raise ValueError(f"Unsupported domain: {domain}")

        models = self._collect_schema_models(module)
        parts = [self._format_schema(model) for model in models]
        return "\n\n".join(parts)

    def _collect_schema_models(self, module: ModuleType) -> list[Type[BaseModel]]:
        models: list[Type[BaseModel]] = []
        for value in module.__dict__.values():
            if (
                isinstance(value, type)
                and issubclass(value, BaseModel)
                and value is not BaseModel
                and value.__module__ == module.__name__
            ):
                models.append(value)
        return sorted(models, key=lambda model: model.__name__)

    def _format_schema(self, model: Type[BaseModel]) -> str:
        schema = model.model_json_schema()
        return (
            f"{model.__name__} schema:\n{json.dumps(schema, indent=2, sort_keys=True)}"
        )
