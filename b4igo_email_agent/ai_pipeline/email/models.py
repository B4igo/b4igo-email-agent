"""Pydantic models for email structure and validation."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, field_validator


class EmailAddress(BaseModel):
    """Email address with optional name."""

    address: EmailStr
    name: Optional[str] = None

    def __str__(self) -> str:
        """String representation of email address."""
        if self.name:
            return f"{self.name} <{self.address}>"
        return self.address

    @classmethod
    def from_any(cls, v: Any) -> "EmailAddress":
        """Build EmailAddress from string, dict, or existing EmailAddress.

        Args:
            v: String address, dict with address/email and optional name,
                or EmailAddress.

        Returns:
            EmailAddress instance.

        Raises:
            ValueError: If v is not a supported type or dict lacks address.
        """
        if isinstance(v, cls):
            return v
        if isinstance(v, str):
            return cls(address=v)
        if isinstance(v, dict):
            return cls(
                address=v.get("address") or v.get("email"),
                name=v.get("name"),
            )
        raise ValueError(f"Invalid email address format: {v}")


class EmailMetadata(BaseModel):
    """Optional email message metadata (IDs, headers, thread, labels)."""

    message_id: Optional[str] = None
    in_reply_to: Optional[str] = None
    references: List[str] = Field(default_factory=list)
    headers: Dict[str, Any] = Field(default_factory=dict)
    thread_id: Optional[str] = None
    labels: List[str] = Field(default_factory=list)


class EmailInput(BaseModel):
    """Input email model from external system."""

    from_address: EmailAddress
    to_address: List[EmailAddress]
    subject: str
    body: str
    received_at: datetime
    metadata: Optional[Union[EmailMetadata, Dict[str, Any]]] = None
    attachments: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    cc: List[EmailAddress] = Field(default_factory=list)
    bcc: List[EmailAddress] = Field(default_factory=list)

    @field_validator("from_address", mode="before")
    @classmethod
    def normalize_from_address(cls, v: Any) -> EmailAddress:
        """Coerce from_address to EmailAddress."""
        return EmailAddress.from_any(v)

    @field_validator("to_address", "cc", "bcc", mode="before")
    @classmethod
    def normalize_address_lists(cls, v: Any) -> List[EmailAddress]:
        """Coerce to/cc/bcc to list of EmailAddress."""
        if v is None:
            return []
        if not isinstance(v, list):
            v = [v]
        return [EmailAddress.from_any(item) for item in v]

    @field_validator("metadata", mode="before")
    @classmethod
    def normalize_metadata(cls, v: Any) -> Optional[EmailMetadata]:
        """Coerce metadata to EmailMetadata or None."""
        if v is None or isinstance(v, EmailMetadata):
            return v
        if isinstance(v, dict):
            return EmailMetadata(**v)
        return None

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
        }
    }
