
# src/message_handler.py
from datetime import datetime
import base64
from googleapiclient.errors import HttpError


def get_email_content(service, message):
   """Extracts email content from a message object."""
   try:
       msg = service.users().messages().get(
           userId='me',
           id=message['id'],
           format='full'
       ).execute()
      
       headers = msg['payload']['headers']
       subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject')
       sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), 'No Sender')
       date_str = next((header['value'] for header in headers if header['name'].lower() == 'date'), '')
       message_id = msg['id']  # Get the message ID for marking as read later
      
       try:
           date_str = ' '.join(date_str.split()[:5])
           date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S')
           formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
       except Exception:
           formatted_date = date_str
      
       if 'parts' in msg['payload']:
           parts = msg['payload']['parts']
           body = ''
           for part in parts:
               if part['mimeType'] == 'text/plain':
                   if 'data' in part['body']:
                       body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                       break
       else:
           if 'data' in msg['payload']['body']:
               body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
           else:
               body = 'No content'
              
       return {
           'id': message_id,
           'subject': subject,
           'sender': sender,
           'date': formatted_date,
           'body': body,
           'snippet': msg['snippet']
       }
   except Exception as e:
       print(f"Error processing message: {str(e)}")
       return None


def get_all_unread_emails(service):
   """Fetches all unread emails."""
   try:
       results = service.users().messages().list(
           userId='me',
           labelIds=['UNREAD', 'INBOX']
       ).execute()
      
       messages = results.get('messages', [])
       if not messages:
           return []
          
       email_list = []
       for message in messages:
           email_content = get_email_content(service, message)
           if email_content:
               email_list.append(email_content)
              
       return email_list
   except Exception as e:
       print(f"Error fetching emails: {str(e)}")
       return []


def mark_as_read(service, message_id):
   """Marks a message as read by removing the UNREAD label."""
   try:
       service.users().messages().modify(
           userId='me',
           id=message_id,
           body={'removeLabelIds': ['UNREAD']}
       ).execute()
       return True
   except Exception as e:
       print(f"Error marking message as read: {str(e)}")
       return False


