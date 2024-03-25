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
    typ, data = connection.fetch(emailNum, 'BODY.PEEK[]')
    if typ == "OK":
        for part in data:
            if isinstance(part, tuple): # Process the raw email content, usually found in part[1]
                header = email.message_from_bytes(part[1])
                subjectLine = header["SUBJECT"]
                print(subjectLine)
                body = getBody(header)
                text = verificationInstance(subjectLine, body)
                if (text):
                    try:
                        messageForwarder.send(connection, emailNum, text.upper())
                    except Exception as e:
                        print(f"Error: {e}")
    else:
        print("Bad processing")
        return None

def verificationInstance(header, body):
    text = f"{header} \n {body}".lower()
    for keyword in keywords:
        if keyword.lower() in text: # Make this stronger, create a minimum score to send
            print("found word")
            return text

def getBody(header):
    if header.is_multipart():
        for part in header.walk():
            # Check if the part is text/plain or text/html, depending on what you want
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode("utf-8")
                return body
        else:
            # Email is not multipart
            body = header.get_payload(decode=True).decode("utf.8")
            return body

