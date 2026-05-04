"""Typed models used by the account manager domain."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal

ProviderType = Literal["imap", "gmail"]
SetupType = Literal["redirect", "boolean", "input", "password"]


@dataclass
class LinkedAccount:
    """Represents a linked provider account for one B4iGO user."""

    id: int
    b4igo_user_id: str
    provider: ProviderType
    email_address: str
    display_name: str | None
    credentials: dict[str, Any]
    config: dict[str, Any]
    created_at: str
    updated_at: str
    last_read: datetime | None = None

    def to_public_dict(self) -> dict[str, Any]:
        """Return a safe representation without secret credential values.

        Returns:
            JSON-safe dictionary for API responses.
        """
        return {
            "id": self.id,
            "b4igoUserId": self.b4igo_user_id,
            "provider": self.provider,
            "emailAddress": self.email_address,
            "displayName": self.display_name,
            "config": self.config,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "credentials": _redact_credentials(self.credentials),
        }


@dataclass
class EmailSetupStep:
    """A step used to configure an email provider account.

    The callback should be a function name for that provider or a full url.
    """

    title: str
    desc: str
    type: SetupType
    value: str | None = None
    callback: str | None = None
    polling_id: str | None = None


@dataclass
class GmailOAuthSession:
    """Persisted OAuth session used to complete Gmail callback safely."""

    state: str
    b4igo_user_id: str
    code_verifier: str
    connector_name: str | None
    created_at: str
    status: str


def _redact_credentials(credentials: dict[str, Any]) -> dict[str, Any]:
    """Redact credential keys that likely contain secrets."""
    redacted: dict[str, Any] = {}
    sensitive_tokens = (
        "password",
        "secret",
        "token",
        "refresh",
        "client_secret",
        "access",
    )
    for key, value in credentials.items():
        if any(token in key.lower() for token in sensitive_tokens):
            redacted[key] = "***"
        else:
            redacted[key] = value
    return redacted
