from dataclasses import dataclass

from b4igo_email_agent.email_connectors.setup_type import SetupType


@dataclass
class EmailSetupStep:
	title: str
	desc: str
	type: SetupType
	callback: str
	value: str #TODO need this?
