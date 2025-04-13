import os
from gmail import authenticate_google_api
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def add_task(title, notes=None, due=None):
    service = authenticate_google_api('tasks', 'v1')

    task = {
        'title': title,
        'notes': notes,
        'due': due  # ISO 8601 format: '2025-04-11T12:00:00.000Z'
    }

    result = service.tasks().insert(tasklist='@default', body=task).execute()
    print(f"Task added: {result['title']} (ID: {result['id']})")

# Example usage
add_task("Finish AI auto-reply project", notes="Make it send witty responses", due="2025-04-12T18:00:00.000Z")
