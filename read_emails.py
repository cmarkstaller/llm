import time
from gmail import *
from deepseek import ask_deepseek

SYSTEM_PROMPT = (
    "Your input is an email I received. I would like your output to strictly be an email response on my behalf. "
    "Your output will be the reply, so respond as if you were me. My name is Chris."
)

def process_email(service, msg_id):
    """Process one email: extract, ask AI, reply, and mark as read."""
    sender, subject, body, thread_id = extract_email_content(service, msg_id)

    email_input = f"From: {sender}\nSubject: {subject}\nBody:\n{body}\n---"
    print("🟢 Processing Email:\n", email_input)

    response_text, thoughts = ask_deepseek(email_input, SYSTEM_PROMPT, print_log=False)

    print("🤖 AI Response:\n", response_text)
    print("💭 Thoughts:\n", thoughts)

    reply = create_reply_message("me", sender, subject, response_text, thread_id)
    service.users().messages().send(userId='me', body=reply).execute()

    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
    print("✅ Replied and marked as read.\n")

def main():
    service = authenticate_google_api('gmail', 'v1')

    while True:
        try:
            print("🔄 Checking for new emails...")
            messages = get_unread_emails(service)
            for msg in messages:
                process_email(service, msg['id'])
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
