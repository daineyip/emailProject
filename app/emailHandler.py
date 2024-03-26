import email
import messageForwarder

keywords = [
    "verification code",
    "security code",
    "authentication",
    "verify your account",
    "verify your email",
    "2FA",
    "two-factor authentication",
    "login attempt",
    "confirmation code"
]
def process_single_email(emailNum, connection):
    # print("fetching data of email")
    try:
        # typ, data = connection.fetch(emailNum, '(BODY.PEEK[])')
        response = connection.fetch(emailNum, ['ENVELOPE', 'BODY.PEEK[]'])
        envelope = response[emailNum][b'ENVELOPE']
        subject = envelope.subject.decode('utf-8', errors='ignore')
        print(f"Subject: {subject}")
        email_raw_bytes = response[emailNum][b'BODY[]']

        message = email.message_from_bytes(email_raw_bytes)
        body = getBody(message)
        print(body)
        text = verificationInstance(subject, body)
        if (text):
            try:
                messageForwarder.send(connection, emailNum, text.upper())
            except Exception as e:
                print(f"Error: {e}")

    except Exception as e:
        print (f"EXCEPTION FOUND: {e}")

def verificationInstance(header, body):
    text = f"{header} \n {body}".lower()
    for keyword in keywords:
        if keyword.lower() in text: # Make this stronger, create a minimum score to send
            print("found word")
            return text

def getBody(email_message):
    # If the email message is multipart
    if email_message.is_multipart():
        # Iterate over each part
        for part in email_message.walk():
            # Focus on text/plain or text/html parts
            if part.get_content_type() in ['text/plain', 'text/html']:
                # Decode and return the payload
                return part.get_payload(decode=True).decode('utf-8', errors='ignore')
    else:
        # For non-multipart emails, directly return the payload
        return email_message.get_payload(decode=True).decode('utf-8', errors='ignore')

