import imaplib
import os
import time
import emailHandler
from datetime import datetime, timedelta

class EmailListener:
    def __init__(self, user, password, server, mailbox):
        print("Initializing")
        self.server = server
        self.user = user
        self.password = password
        self.mailbox = mailbox
        self.connection = self.connect()

    def connect(self):
        try:
            print("Attempting to connect")
            self.connection = imaplib.IMAP4_SSL(self.server)
            print("Connected to gmail")
            self.connection.login(self.user, self.password)
            print("Connected to personal account")
            self.connection.select(self.mailbox)
            print("Connected to 'inbox'")
            return self.connection
        except Exception as e:
            print("Error occurred in connecting: {e}")
            return None


    def codeListener(self): # change criteria to be of specific subject line
        messages = self.getRelevantEmails()
        for num in messages:
            emailHandler.process_single_email(num[0], self.connection)
        return

    def getRelevantEmails(self): #Retrieve most recent emails
        emails = []
        date = (datetime.today() - timedelta(days=1)).strftime("%d-%b-%Y")
        search_criteria = f'(UNSEEN SINCE "{date}")'
        status, messages = self.connection.search(None, search_criteria)
        if status == "OK":
            decoded_messages = self.decodeMessages(messages)
            print(decoded_messages)
            print(decoded_messages[0].split())
            for num in decoded_messages:
                result, fetch_data = self.connection.fetch(num, '(INTERNALDATE)')
                if result == "OK":
                    print("result OK from fetching internal date emails")
                    emails.append((num, self.handleInternalDateMessage(fetch_data)))
                else:
                    print("Error with fetching email dates")
                    return
            sorted_emails = sorted(emails, key=lambda x: datetime.strptime(x[1], "%d-%b-%Y %H:%M:%S %z"), reverse=True)
            print(sorted_emails)
            return sorted_emails
        else:
            print("Error with retrieving messages")
            return

    def handleInternalDateMessage(self, data):
        print(data[0])
        date = self.getEmailDate(data)
        print(date)
        # email_data = data[1]
        # print("email data is:" + email_data)
        # email_date_str = email_data.decode()
        # print("email date string is:" + email_date_str)
        # date = self.getEmailDate(email_date_str)
        # print("email date:" + date)
        return date

    def getEmailDate(self, data):
        print("in getEmail")
        print(data)
        if data: # Extract the internal date from the response
            decodedEmail = data[0].decode()  # The internal date is typically enclosed in double quotes
            print(decodedEmail)
            parts = decodedEmail.split('"')
            print(parts[1])
            return parts[1]

    def decodeMessages(self, messages):
        if messages and isinstance(messages[0], bytes): # Decode the byte string to a regular string and then split
            message_ids = messages[0].decode().split()
            for n in message_ids:
                print("decodeMessages: " + n)
            return message_ids
        else:
            print("No messages or messages are not in the expected format.")
            return
    def run(self):
        if self.connection is None:
            print("Failed to connect to mailbox")
            return
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
