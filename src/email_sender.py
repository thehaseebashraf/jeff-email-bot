# email_sender.py
from email.mime.text import MIMEText
import base64


# def create_reply_message(original_email, reply_text):
#    """Creates a reply message in Gmail-compatible format with the original message quoted."""
#    original_date = original_email['date']
#    original_sender = original_email['sender']
#    original_subject = original_email['subject']
#    original_body = original_email.get('body', original_email['snippet'])


<<<<<<< HEAD
   full_message = (
       f"{reply_text}\n\n"
       f"On {original_date}, {original_sender} wrote:\n"
       f"  Subject: {original_subject}\n"
       f"  {original_body.replace('\n', '\n  ')}")
=======
#    full_message = (
#        f"{reply_text}\n\n"
#        f"On {original_date}, {original_sender} wrote:\n"
#        f"  Subject: {original_subject}\n"
#        f"  {original_body.replace('\n', '\n  ')}"
#    )
>>>>>>> 635519d132d865d343bc33ca322c8b54771e99c9


#    message = MIMEText(full_message)
#    message['to'] = original_email['sender']
#    message['subject'] = f"Re: {original_email['subject']}"
  
#    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
#    return {'raw': raw}
def create_reply_message(original_email, reply_text):
    """Creates a reply message in Gmail-compatible format with the original message quoted."""
    original_date = original_email['date']
    original_sender = original_email['sender']
    original_subject = original_email['subject']
    original_body = original_email.get('body', original_email['snippet'])

    # Fixed the newline handling
    quoted_body = original_body.replace('\n', '\n  ')
    
    full_message = (
        f"{reply_text}\n\n"
        f"On {original_date}, {original_sender} wrote:\n"
        f"  Subject: {original_subject}\n"
        f"  {quoted_body}")

    message = MIMEText(full_message)
    message['to'] = original_email['sender']
    message['subject'] = f"Re: {original_email['subject']}"
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw}
   

def send_reply(service, message):
   """Sends the reply email."""
   try:
       sent_message = service.users().messages().send(
           userId='me',
           body=message
       ).execute()
       return sent_message
   except Exception as e:
       print(f"An error occurred while sending: {e}")
       return None


