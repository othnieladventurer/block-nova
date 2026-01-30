from twilio.rest import Client
import os

# Load environment variables
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # your Twilio sandbox number

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number, message):
    """
    Send a WhatsApp message using Twilio.
    
    Args:
        to_number (str): WhatsApp number including country code, e.g., '+33712345678'
        message (str): Message content
    """
    if not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"

    from_number = f"whatsapp:{TWILIO_WHATSAPP_NUMBER}"

    try:
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        return message.sid
    except Exception as e:
        print("Error sending WhatsApp message:", e)
        return None
