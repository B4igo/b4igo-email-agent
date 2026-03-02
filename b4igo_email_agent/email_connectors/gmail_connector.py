from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json
from datetime import datetime
from b4igo_email_agent.email_connectors.email import Email


def get_credentials_from_token(tokenJson: str) -> Credentials:
    """Load and refresh credentials from stored token JSON."""
    token_data = json.loads(tokenJson)

    creds = Credentials(
        token=token_data['token'],
        refresh_token=token_data['refresh_token'],
        token_uri=token_data['token_uri'],
        client_id=token_data['client_id'],
        client_secret=token_data['client_secret'],
        scopes=token_data['scopes']
    )

    if creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())

    return creds


def handle_oauth_callback(auth_code: str, client_secrets_file: str, redirect_uri: str, state: str = None, code_verifier: str = None) -> str:
    """Exchange authorization code for tokens and return as JSON string."""
    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=['https://www.googleapis.com/auth/gmail.readonly'],
        redirect_uri=redirect_uri,
        state=state
    )

    if code_verifier:
        flow.code_verifier = code_verifier

    flow.fetch_token(code=auth_code)
    creds = flow.credentials

    token_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

    return json.dumps(token_data)


def get_authorization_url(client_secrets_file: str, redirect_uri: str) -> tuple[str, str, str]:
    """Generate OAuth URL for user to authorize access.

	Returns:
		Tuple of (auth_url, state, code_verifier) - state and code_verifier should be stored and used in callback
	"""
    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=['https://www.googleapis.com/auth/gmail.readonly'],
        redirect_uri=redirect_uri
    )

    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    return auth_url, state, flow.code_verifier


def get_user_email_from_token(tokenJson: str) -> str:
    """Get the user's email address from their Gmail token."""
    creds = get_credentials_from_token(tokenJson)
    service = build('gmail', 'v1', credentials=creds)

    profile = service.users().getProfile(userId='me').execute()
    return profile['emailAddress']


def get_inbox_since_date(since: datetime, tokenJson: str) -> list[Email]:
    """Fetch emails from Gmail inbox since specified date."""
    creds = get_credentials_from_token(tokenJson)
    service = build('gmail', 'v1', credentials=creds)

    query = f'after:{int(since.timestamp())}'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        emails.append(_parse_gmail_message_to_email(full_msg))

    return emails


def _parse_gmail_message_to_email(gmail_msg: dict) -> Email:
    """Convert Gmail API message format to Email dataclass."""
    headers = {h['name']: h['value'] for h in gmail_msg['payload']['headers']}

    return Email(
        from_address=headers.get('From', ''),
        to_addresses=_parse_email_addresses(headers.get('To', '')),
        subject=headers.get('Subject', ''),
        body=_extract_body(gmail_msg['payload']),
        date=datetime.fromtimestamp(int(gmail_msg['internalDate']) / 1000),
        message_id=gmail_msg['id'],
        thread_id=gmail_msg.get('threadId'),
        cc=_parse_email_addresses(headers.get('Cc', '')) if headers.get('Cc') else None,
        bcc=_parse_email_addresses(headers.get('Bcc', '')) if headers.get('Bcc') else None
    )


def _parse_email_addresses(address_string: str) -> list[str]:
    """Parse comma-separated email addresses, handling display names."""
    if not address_string:
        return []

    import re
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    emails = re.findall(email_pattern, address_string)

    return emails if emails else []


def _extract_body(payload: dict) -> str:
    """Extract email body from Gmail message payload."""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                import base64
                return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    elif 'body' in payload and 'data' in payload['body']:
        import base64
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return ''