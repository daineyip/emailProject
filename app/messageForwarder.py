from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH = os.getenv("TWILIO_AUTH_TOKEN")
VIRTUAL_PHONE = os.getenv("TWILIO_VIRTUAL_NUMBER")
DELIVERY_PHONE = os.getenv("DELIVERY_NUMBER")

def send(forward_message):  # 'forward_message' is the message you want to forward
    account_sid = SID  # Replace 'your_account_sid' with your actual Twilio Account SID
    auth_token = AUTH    # Replace 'your_auth_token' with your actual Twilio Auth Token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=VIRTUAL_PHONE,  # Replace '+1234567890' with your Twilio phone number
        body=forward_message,  # Use the 'forward_message' parameter for the message body
        to=DELIVERY_PHONE       # Replace '+0987654321' with the recipient's phone number
    )