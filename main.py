# main.py
from src.auth import get_gmail_service
from src.message_handler import get_all_unread_emails, mark_as_read
from src.email_sender import create_reply_message, send_reply
from src.vector_db import search_similar_content
from src.response_generator import generate_email_response
from googleapiclient.errors import HttpError
import time

def main():
    """Main function to read and reply to all unread emails."""
    try:
        print("Connecting to Gmail...", flush=True)
        service = get_gmail_service()
        print("Connected successfully!")
        
        unread_emails = get_all_unread_emails(service)
        
        if not unread_emails:
            print("\nNo unread messages in your inbox.")
            return
            
        print(f"\nFound {len(unread_emails)} unread messages.")
        
        for index, email_data in enumerate(unread_emails, 1):
            print(f"\nProcessing email {index} of {len(unread_emails)}")
            print("-" * 70)
            print(f"From: {email_data['sender']}")
            print(f"Date: {email_data['date']}")
            print(f"Subject: {email_data['subject']}")
            print("\nPreview:")
            print(email_data['snippet'])
            print("-" * 70)
            
            # Search for similar content
            print("\nSearching for similar content...")
            search_text = f"{email_data['subject']} {email_data.get('body', email_data['snippet'])}"
            similar_content = search_similar_content(search_text)
            
            # Generate response using OpenAI
            print("Generating response...")
            reply_text = generate_email_response(
                email_data['subject'],
                email_data.get('body', email_data['snippet']),
                similar_content
            )
            
            # Create and send reply
            reply_message = create_reply_message(email_data, reply_text)
            
            print("Sending reply...", flush=True)
            sent_message = send_reply(service, reply_message)
            
            if sent_message:
                print("Reply sent successfully!")
                if mark_as_read(service, email_data['id']):
                    print("Marked as read.")
                else:
                    print("Failed to mark as read.")
            else:
                print("Failed to send reply.")
            
            if index < len(unread_emails):
                print("\nWaiting briefly before processing next email...")
                time.sleep(2)
                
    except HttpError as error:
        print(f"An API error occurred: {error}")
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        print("\nEmail processing completed.")

if __name__ == '__main__':
    main()