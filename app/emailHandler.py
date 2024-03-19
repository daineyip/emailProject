import email
def process_single_email(emailNum, connection):
    print("fetching data of email")
    typ, data = connection.fetch(emailNum, '(RFC822)')
    if typ == "OK":
        for part in data:
            if isinstance(part, tuple): # Process the raw email content, usually found in part[1]
                email_message = email.message_from_bytes(part[1])
                body = email_message.get_payload(decode=True)
                print(email_message["Subject"])
                print(email_message["From"])
                print(email_message["To"])
                print(body)
    else:
        print("Bad processing")
        return None