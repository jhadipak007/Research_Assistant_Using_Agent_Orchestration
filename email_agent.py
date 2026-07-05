from agents import Agent, function_tool, ModelSettings
from dotenv import load_dotenv
from send_email import send_email
import os

load_dotenv(override=True)

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")
USE_EMAIL= os.getenv("USE_EMAIL", "true").lower() == "true"

@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """
    Send out an email with the given subject and body. 

    Args: 
        subject: The subject of the email
        text_body: The body of the email as plain text
        html_body: The HTML body of the email.
    """

    print("----------  Executing send email tool ---------- \n\n")
    if True:
        response = send_email(subject=subject, html_body=html_body) 
        # print(f"Email Subject: {subject}\n\n")
        # print(f"Email body: {text_body}\n\n")
        # print(f"Email HTML Body: {html_body}")
    
    return "Email Sent Successfully" if response.status_code == 200 else "Error during Sending Email."

INSTRUCTIONS= """
You are provided with a detailed report. Use your tool to send an email, converting the report into a clean, well presented HTML email with an appropriate subject line.
"""

settings = ModelSettings(tool_choice="required")

email_agent = Agent(name="Email Agent", instructions=INSTRUCTIONS, model=MODEL_NAME, tools=[send_email_tool], model_settings=settings)
