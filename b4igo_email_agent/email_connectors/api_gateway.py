# main file to look at for this module. generic calls to this file figures out what connector to use and returns generic data.
from datetime import datetime
from b4igo_email_agent.email_connectors.connector_types import ConnectorType
from b4igo_email_agent.email_connectors.gmail_connector import (
    get_inbox_since_date as get_gmail_emails,
    get_authorization_url as get_gmail_auth_url,
    get_user_email_from_token as get_gmail_email,
)
from b4igo_email_agent.email_connectors.email import Email


def get_connector_types() -> list[str]:
    """Get list of all available connector types."""
    return [enum.value for enum in ConnectorType]


def get_emails_from_connector(
        connector_type: str, token_json: str, since: datetime
) -> list[Email]:
    """Get emails from a connector since a specific date."""
    if connector_type == ConnectorType.GMAIL.value:
        return get_gmail_emails(since, token_json)
    # TODO: Add other connectors
    return []


def get_authorization_url(
        connector_type: str, client_secrets_file: str, redirect_uri: str
) -> tuple[str, str, str]:
    """Get OAuth authorization URL for a connector type."""
    if connector_type == ConnectorType.GMAIL.value:
        return get_gmail_auth_url(client_secrets_file, redirect_uri)
    # TODO: Add other connectors
    raise ValueError(f"Unsupported connector type: {connector_type}")


def extract_email_from_token(connector_type: str, token_json: str) -> str:
    """Extract email address from connector token."""
    if connector_type == ConnectorType.GMAIL.value:
        return get_gmail_email(token_json)
    # TODO: Add other connectors
    raise ValueError(f"Unsupported connector type: {connector_type}")