from email.mime.text import MIMEText
from googleapiclient.discovery import build
import base64


def send_email(subject, recipient, body, creds):
    message = MIMEText(body)
    message['to'] = recipient
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service = build('gmail', 'v1', credentials=creds)
    message = {
        'raw': raw
    }

    service.users().messages().send(userId='me', body=message).execute()
