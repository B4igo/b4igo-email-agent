from dataclasses import dataclass
from datetime import datetime

from b4igo_email_agent.email_connectors.connector_types import ConnectorType

@dataclass
class ConnectorInfo:
	username: str
	connectorType: ConnectorType
	connectorName: str
	tokenJson: str
	lastRead: datetime | None = None
	lastErrorMsg: str | None = None

