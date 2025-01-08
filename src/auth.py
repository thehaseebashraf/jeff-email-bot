
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
         'https://www.googleapis.com/auth/gmail.send',
         'https://www.googleapis.com/auth/gmail.modify'  # Added this scope for marking as read
]


def get_gmail_service():
   """Sets up Gmail API service with proper authentication."""
   creds = None
  
   if os.path.exists('gmail_token.pickle'):
       with open('gmail_token.pickle', 'rb') as token:
           creds = pickle.load(token)
  
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file('gmail_credentials.json', SCOPES)
           creds = flow.run_local_server(port=0)
      
       with open('gmail_token.pickle', 'wb') as token:
           pickle.dump(creds, token)


   return build('gmail', 'v1', credentials=creds)



