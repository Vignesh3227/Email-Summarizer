from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
SCOPES=["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE ="token_gmail_v1.json"

def authenticate_gmail():
    creds=None
    if os.path.exists(TOKEN_FILE):
        creds=Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        flow=InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds=flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def get_unread_emails():
    service=authenticate_gmail()
    results=service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread",maxResults=10).execute()
    messages=results.get("messages", []) 
    email_data=[]
    for msg in messages: 
        msg_details=service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers=msg_details.get("payload", {}).get("headers", [])
        subject=next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender=next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")
        
        email_data.append({"subject": subject, "sender": sender})   
    return {"unread_emails": email_data}
