from dotenv import load_dotenv
import os

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


# --------------------------------------------------------------
# List Template WhatsApp message
# --------------------------------------------------------------
def list_template():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": '',
        "type": "interactive",
        "interactive": 
        {
            "type": "list",
            "body": 
            {
            "text": "Please select a city from the following:"
            },
            "action": 
            {
                "button": "Options",
                "sections": 
                [
                    {
                        "title": "Choose",
                        "rows": 
                        [
                            
                        ]
                    }
                ]
            }
        }
    }

    return url, headers,data

# --------------------------------------------------------------
# Text Template WhatsApp message
# --------------------------------------------------------------

def text_template():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": '',
        "text": {
        "body": ""
     }
    }

    return url, headers,data