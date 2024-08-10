import requests
import os
from dotenv import load_dotenv

load_dotenv()

IPQUALITYSCORE_API_KEY = os.environ.get("IPQUALITYSCORE_API_KEY")

def is_vpn_ip(ip_address):
    API_URL = f"https://www.ipqualityscore.com/api/json/ip/{IPQUALITYSCORE_API_KEY}/{ip_address}"
    print(API_URL)
    response = requests.get(API_URL)
    data = response.json()
    return data.get('vpn', False)

