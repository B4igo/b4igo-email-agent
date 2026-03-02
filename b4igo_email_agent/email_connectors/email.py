from dataclasses import dataclass
from datetime import datetime

@dataclass
class Email:
	from_address: str
	to_addresses: list[str]
	subject: str
	body: str
	date: datetime
	message_id: str
	is_read: bool = False
	labels: list[str] | None = None
	thread_id: str | None = None
	email_url: str | None = None
	cc: list[str] | None = None
	bcc: list[str] | None = None