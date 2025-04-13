import os.path
import base64
from deepseek import *
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import email

# Gmail API scope for read-only access
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
# SYSTEM_PROMPT = "You are an email assistant. You look at emails that arrive in my inbox, and reply to them if they require a response. To be clear, the prompts I am giving you are emails from my inbox. If they do not seem like they require a response, simply respond with NULL. You may come accross questions in these emails that you need more information from me as the user on. If you have any questions about what I might want or prefer, simply respond with a json object in the form of {type: email, question: <your question goes here>}. Otherwise, respond on my behalf."
SYSTEM_PROMPT = "Your input is an email I received. I would like your output to strictly be an email response on my behalf. Your output will be the reply, so respond as if you were me. My name is Chris."

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_message(sender, to, subject, message_text, thread_id):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = f"Re: {subject}"
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {
        'raw': raw_message,
        'threadId': thread_id
    }

# Create and send the reply


def get_emails():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    
    # 👇 Get only UNREAD emails from the Primary inbox
    results = service.users().messages().list(
        userId='me',
        q='is:unread category:primary',
        maxResults=5
    ).execute()
    
    messages = results.get('messages', [])
    
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload['headers']
        sender, subject = '', ''
        for d in headers:
            if d['name'] == 'From':
                sender = d['value']
            if d['name'] == 'Subject':
                subject = d['value']
        parts = payload.get('parts', [])
        if parts:
            body = parts[0]['body']['data']
            data = base64.urlsafe_b64decode(body.encode('ASCII')).decode('utf-8')
        else:
            data = payload['body']['data']
            data = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
        
        # ✅ Mark the email as read
        service.users().messages().modify(
            userId='me',
            id=msg['id'],
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        
        deep_seek_input = f"From: {sender}\nSubject: {subject}\nBody:\n{data}\n---"

        print(deep_seek_input)

        clean, think = ask_deepseek(deep_seek_input, SYSTEM_PROMPT, print_log=False)

        print("Deep Seek")
        print(clean)
        print(think)

        print("Sending email")
        
        reply = create_message(
        sender="me",
        to=sender,
        subject=subject,
        message_text=clean,
        thread_id=txt['threadId']
        )

        service.users().messages().send(userId="me", body=reply).execute()

import time

if __name__ == "__main__":
    while True:
        try:
            print("Checking emails...")
            get_emails()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)