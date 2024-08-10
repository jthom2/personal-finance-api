import requests
import os
from dotenv import load_dotenv

load_dotenv()

MAILBOXVALIDATOR_API_KEY = os.environ.get("MAILBOXVALIDATOR_API_KEY")

def is_tempmail(email, api_key):
    response = requests.get(f"https://api.mailboxvalidator.com/v1/validation/single?key={api_key}&email={email}")
    data = response.json()
    return data.get('is_disposable', False)