import imaplib
import os
import time
from email.utils import parsedate_to_datetime

from imapclient import IMAPClient
import emailHandler
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL_USERNAME")
PASS = os.getenv("EMAIL_PASSWORD")
SERVER = 'imap.gmail.com'

class EmailListener:
    def fetch_most_recent_email(self, client):
        # Assuming 'use_uid=True' so UIDs are returned
        unseen_messages = client.search('UNSEEN')
        if unseen_messages:
            most_recent_uid = max(unseen_messages)  # Get the highest UID, which is the most recent
            response = client.fetch(most_recent_uid, ['ENVELOPE', 'BODY.PEEK[]'])
            envelope = response[most_recent_uid][b'ENVELOPE']
            subject = envelope.subject.decode()
            print(f"Most recent email subject: {subject}")
            emailHandler.process_single_email(most_recent_uid, client)
        else:
            print("No unseen messages found.")

    def main(self):
        with IMAPClient(SERVER, use_uid=True, ssl=True) as client:
            client.login(EMAIL, PASS)
            client.select_folder('INBOX')
            print("Entering IDLE mode. Waiting for new messages...")

            try:
                client.idle()
                while True:
                    responses = client.idle_check(timeout=30)
                    if responses:  # This means there's new activity
                        print("New activity detected.")
                        client.idle_done()  # Necessary to temporarily exit IDLE mode to fetch emails

                        self.fetch_most_recent_email(client)  # Fetch and process the most recent email

                        client.idle()  # Re-enter IDLE mode to continue waiting for new messages
                    else:
                        print("No new activity. Re-checking...")

            except KeyboardInterrupt:
                print("Exiting...")
                client.idle_done()

if __name__ == "__main__":
    emailListener = EmailListener()
    emailListener.main()