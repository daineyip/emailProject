import imaplib
import os
import time
import email
from email.header import decode_header

class EmailListener:
    def __init__(self, user, password, server, mailbox):
        print("Initializing")
        self.server = server
        self.user = user
        self.password = password
        self.mailbox = mailbox
        self.connection = self.connect()

    def connect(self):
        print("Attempting to connect")
        self.connection = imaplib.IMAP4_SSL(self.server)
        print("Connected to gmail")
        self.connection.login(self.user, self.password)
        print("Connected to personal account")
        self.connection.select(self.mailbox)
        print("Connected to 'inbox'")

    def codeListener(self, criteria='UNSEEN'):
        status, messages = self.connection.search(None, criteria)
        return messages

    def run(self):
        while True:
            print("Running")
            self.codeListener()
            time.sleep(60)  # Wait for 1 minute before checking

if __name__ == "__main__":
    user = os.getenv("USER")
    password = os.getenv("PASS")
    server = 'imap.gmail.com'
    mailbox = 'inbox'

    listener = EmailListener(user, password, server, mailbox)
    listener.run()
