"""Email content extraction and parsing with Pydantic validation."""

import logging
from email.message import EmailMessage
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from typing import Any, Dict, List, Union

from pydantic import ValidationError

from .models import EmailAddress, EmailInput

logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup

    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    logger.warning(
        "BeautifulSoup4 (bs4) not available. HTML parsing will use fallback parser."
    )


def email_message_to_input(msg: EmailMessage) -> EmailInput:
    """Convert stdlib EmailMessage to EmailInput for pipeline use.

    Parses From/To/Cc/Bcc, Subject, body (plain preferred), and date.
    Uses extract_text_content for HTML bodies so text matches classifier input.
    """
    from_raw = msg.get("from", "") or ""
    from_addr = (
        normalize_address(from_raw)
        if from_raw
        else EmailAddress(address="unknown@unknown")
    )
    to_raw = msg.get_all("to") or []
    to_address: List[EmailAddress] = [
        normalize_address(addr) for addr in to_raw if isinstance(addr, str)
    ]
    cc_raw = msg.get_all("cc") or []
    cc_list: List[EmailAddress] = [
        normalize_address(addr) for addr in cc_raw if isinstance(addr, str)
    ]
    bcc_raw = msg.get_all("bcc") or []
    bcc_list: List[EmailAddress] = [
        normalize_address(addr) for addr in bcc_raw if isinstance(addr, str)
    ]
    subject = msg.get("subject", "") or ""
    body = ""
    if msg.is_multipart():
        body_part = msg.get_body(preferencelist=("plain",))
        if body_part is not None:
            raw = body_part.get_content()
            body = extract_text_content(raw) if raw else ""
    else:
        raw = msg.get_content()
        body = extract_text_content(raw) if raw else ""

    date_header = msg.get("date")
    if date_header:
        try:
            received_at = parsedate_to_datetime(date_header)
        except Exception:
            from datetime import datetime

            received_at = datetime.now()
    else:
        from datetime import datetime

        received_at = datetime.now()

    return EmailInput(
        from_address=from_addr,
        to_address=to_address,
        subject=subject,
        body=body,
        received_at=received_at,
        cc=cc_list,
        bcc=bcc_list,
    )


def email_input_to_message(email: EmailInput) -> EmailMessage:
    """Convert EmailInput to stdlib EmailMessage for DomainClassifier.classify().

    Builds a minimal MIME message with From, To, Subject, body so the classifier
    sees the same text it would from a raw message. Keeps domain_classifier
    unchanged.
    """
    message = EmailMessage()
    message["From"] = str(email.from_address)
    message["To"] = ", ".join(str(addr) for addr in email.to_address)
    if email.cc:
        message["Cc"] = ", ".join(str(addr) for addr in email.cc)
    if email.bcc:
        message["Bcc"] = ", ".join(str(addr) for addr in email.bcc)
    message["Subject"] = email.subject
    message.set_content(email.body or "")
    if hasattr(email.received_at, "strftime"):
        from email.utils import format_datetime

        message["Date"] = format_datetime(email.received_at)
    return message


class HTMLTextExtractor(HTMLParser):
    """Simple HTML parser to extract text content."""

    def __init__(self):
        """Initialize the parser state."""
        super().__init__()
        self.text = []
        self.skip_tags = {"script", "style", "head", "meta"}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        """Record current tag for filtering."""
        self.current_tag = tag.lower()

    def handle_endtag(self, tag):
        """Clear current tag."""
        self.current_tag = None

    def handle_data(self, data):
        """Append text from non-skipped tags."""
        if self.current_tag not in self.skip_tags:
            self.text.append(data.strip())

    def get_text(self) -> str:
        """Get extracted text content."""
        return " ".join(self.text)


def normalize_address(
    address: Union[str, EmailAddress, Dict[str, Any]]
) -> EmailAddress:
    """Normalize email address to EmailAddress model.

    Args:
        address: Email address in various formats

    Returns:
        EmailAddress instance
    """
    if isinstance(address, EmailAddress):
        return address

    if isinstance(address, str):
        # Try to parse "Name <email@example.com>" format
        if "<" in address and ">" in address:
            name_part = address[: address.index("<")].strip().strip("\"'")
            email_part = address[address.index("<") + 1 : address.index(">")].strip()
            return EmailAddress(
                address=email_part, name=name_part if name_part else None
            )
        return EmailAddress(address=address)

    if isinstance(address, dict):
        # Handle dict format
        email = (
            address.get("address")
            or address.get("email")
            or address.get("emailAddress")
        )
        name = address.get("name") or address.get("displayName")
        if email:
            return EmailAddress(address=email, name=name)
        raise ValueError(f"Cannot extract email address from dict: {address}")

    raise ValueError(f"Unsupported address format: {type(address)}")


def extract_text_content(body: str) -> str:
    """Extract plain text from HTML email body.

    Args:
        body: Email body (may be HTML or plain text)

    Returns:
        Plain text content
    """
    if not body:
        return ""

    # Check if body contains HTML tags
    if "<html" in body.lower() or "<body" in body.lower() or "<div" in body.lower():
        # Try BeautifulSoup if available
        if BEAUTIFULSOUP_AVAILABLE:
            try:
                soup = BeautifulSoup(body, "html.parser")

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Get text and clean up
                text = soup.get_text()

                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (
                    phrase.strip() for line in lines for phrase in line.split("  ")
                )
                text = " ".join(chunk for chunk in chunks if chunk)

                return unescape(text)
            except Exception as e:
                logger.warning(
                    f"Failed to parse HTML with BeautifulSoup: {e}, using fallback"
                )

        # Fallback to simple parser
        parser = HTMLTextExtractor()
        parser.feed(body)
        return parser.get_text()

    # Already plain text
    return body.strip()


def parse_email(json_data: Dict[str, Any]) -> EmailInput:
    """Parse and validate JSON email data using Pydantic models.

    Args:
        json_data: Dictionary containing email data

    Returns:
        Validated EmailInput instance

    Raises:
        ValidationError: If email data is invalid
    """
    try:
        # Normalize addresses if they're strings
        if "from_address" in json_data and isinstance(json_data["from_address"], str):
            json_data["from_address"] = normalize_address(
                json_data["from_address"]
            ).model_dump()

        if "to_address" in json_data:
            to_addr = json_data["to_address"]
            if isinstance(to_addr, str):
                json_data["to_address"] = [normalize_address(to_addr).model_dump()]
            elif isinstance(to_addr, list):
                json_data["to_address"] = [
                    (
                        normalize_address(addr).model_dump()
                        if isinstance(addr, str)
                        else addr
                    )
                    for addr in to_addr
                ]

        # Extract text from HTML body if needed
        if "body" in json_data:
            json_data["body"] = extract_text_content(json_data["body"])

        # Create and validate EmailInput
        email = EmailInput(**json_data)

        logger.debug(f"Successfully parsed email: {email.subject}")
        return email

    except ValidationError as e:
        logger.error(f"Email validation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error parsing email: {e}", exc_info=True)
        raise ValueError(f"Failed to parse email: {str(e)}") from e


def validate_email(email: EmailInput) -> bool:
    """Perform additional validation on parsed email.

    Args:
        email: EmailInput instance to validate

    Returns:
        True if email is valid, False otherwise
    """
    # Check that email has required content
    if not email.subject or not email.subject.strip():
        logger.warning("Email missing subject")
        return False

    if not email.body or not email.body.strip():
        logger.warning("Email missing body")
        return False

    # Validate that we have at least one recipient
    if isinstance(email.to_address, str):
        if not email.to_address.strip():
            return False
    elif isinstance(email.to_address, list):
        if len(email.to_address) == 0:
            return False

    return True


def format_email_for_llm(email: EmailInput) -> str:
    """Format email data as a string for LLM processing.

    Args:
        email: EmailInput instance

    Returns:
        Formatted string representation of the email
    """
    # Format from address
    from_str = (
        str(email.from_address)
        if isinstance(email.from_address, EmailAddress)
        else email.from_address
    )

    # Format to address(es)
    if isinstance(email.to_address, list):
        to_str = ", ".join(
            str(addr) if isinstance(addr, EmailAddress) else addr
            for addr in email.to_address
        )
    else:
        to_str = (
            str(email.to_address)
            if isinstance(email.to_address, EmailAddress)
            else email.to_address
        )

    # Format date
    date_str = (
        email.received_at.isoformat()
        if hasattr(email.received_at, "isoformat")
        else str(email.received_at)
    )

    return f"""Subject: {email.subject}
From: {from_str}
To: {to_str}
Date: {date_str}

{email.body}"""
