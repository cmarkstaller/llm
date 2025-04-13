import os.path
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os


SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/tasks'
]

def authenticate_google_api(api_name, api_version):
    """Authenticate and return a service object for the specified Google API."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build(api_name, api_version, credentials=creds)

def get_unread_emails(service, max_results=5):
    """Retrieve a list of unread messages in the primary inbox."""
    results = service.users().messages().list(
        userId='me',
        q='is:unread category:primary',
        maxResults=max_results
    ).execute()
    return results.get('messages', [])

def extract_email_content(service, msg_id):
    """Extract sender, subject, body, and thread ID from an email."""
    msg = service.users().messages().get(userId='me', id=msg_id).execute()
    payload = msg['payload']
    headers = payload['headers']

    sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
    thread_id = msg.get('threadId', '')

    body = ''
    parts = payload.get('parts', [])
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body_data = part['body'].get('data')
                if body_data:
                    body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    break
    else:
        body_data = payload['body'].get('data')
        if body_data:
            body = base64.urlsafe_b64decode(body_data).decode('utf-8')

    return sender, subject, body, thread_id

def create_reply_message(sender, to, subject, message_text, thread_id):
    """Create a MIMEText reply and return it in Gmail API sendable format."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = f"Re: {subject}"
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {
        'raw': raw_message,
        'threadId': thread_id
    }