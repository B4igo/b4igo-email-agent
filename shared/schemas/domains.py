"""Domain type and the mapping from each domain to its schema module.

This is the single source of truth for the set of supported domains and the
schema module each one parses into. It deliberately avoids importing the AI
pipeline (and its heavy sentence-transformers dependency) so that schema and
prompt code can be imported and tested without the ML stack.
"""

from types import ModuleType
from typing import Literal

from shared.schemas import education_schemas, legal_schemas, personal_schemas, schemas

Domain = Literal["education", "health", "legal", "personal", "other"]

# Domains that have a parser schema module. "other" is intentionally absent:
# it is the catch-all for messages with no structured schema to extract.
DOMAIN_MODULES: dict[Domain, ModuleType] = {
    "education": education_schemas,
    "health": schemas,
    "legal": legal_schemas,
    "personal": personal_schemas,
}
