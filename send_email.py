from dotenv import load_dotenv
import os
import requests

load_dotenv()
APPIAN_BASE_URL = os.getenv("APPIAN_ENV_BASE_URL")
APPIAN_API_KEY = os.getenv("APPIAN_API_KEY")


def send_email(subject: str, html_body: str, to: str):
    endpoint_url = f"{APPIAN_BASE_URL}" + "/send-email"
    headers = {
        "Appian-API-Key": APPIAN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "subject": subject,
        "emailBody": html_body,
        "to": to
    }
    print("Calling Appian To Send Email")
    response = requests.post(endpoint_url, headers=headers, json=payload)
    print(f"Appian responded with a status code of {response.status_code}")
    response.raise_for_status()
    return response
