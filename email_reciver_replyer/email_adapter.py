
import imaplib
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import email
from config import (SMTP_SERVER, SMTP_PORT, 
                    SMTP_USER, SMTP_PASSWORD, 
                    FROM_EMAIL,IMAP_PORT,
                     IMAP_SERVER, EMAIL_ACCOUNT )
from dotenv import load_dotenv
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header

# Load environment variables from .env
load_dotenv()

# Set up Jinja2 environment
template_dir = "templates"  # Folder where templates are stored
env = Environment(loader=FileSystemLoader(template_dir))


def connect_to_imap():
    try:
        # Establish connection to IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, SMTP_PASSWORD)
        mail.select("inbox")  # Connect to inbox
        return mail
    except Exception as e:
        print(f"Error connecting to IMAP server: {e}")
        return None

def send_email(to_email, subject, template_name, context):
    # Render the template with the context data
    template = env.get_template(template_name)
    html_content = template.render(context)
    
    # Create email message
    email = EmailMessage()
    email['From'] = FROM_EMAIL
    email['To'] = to_email
    email['Subject'] = subject
    email.set_content(html_content, "html")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()  # Encrypt the communication
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(email)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


def check_for_new_emails():
    mail = connect_to_imap()
    if not mail:
        return

    # Search for all emails that are unseen (unread)
    status, messages = mail.search(None, 'UNSEEN')
    if status != "OK":
        print("No new messages.")
        return

    # Get the list of email IDs
    email_ids = messages[0].split()
    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                from_email = msg.get("From")
                
                print(f"New email from: {from_email} with subject: {subject}")

                # Check for specific content in the email subject/body to trigger responses
                if "confirmation" in subject.lower():
                    send_confirmation_email(from_email)
                elif "password reset" in subject.lower():
                    send_password_reset_email(from_email)
                elif "payment" in subject.lower():
                    send_payment_confirmation_email(from_email)
                else:
                    print("No specific action found for this email.")




def send_confirmation_email(to_email):
    context = {
        'name': 'User',  # Customize this with dynamic data if needed
    }
    send_email(to_email, "Your Confirmation Email", "confirmation_email.html", context)


def send_password_reset_email(to_email):
    context = {
        'name': 'User',
        'reset_link': "http://example.com/reset-password?token=1234567890",  # Replace with real link
    }
    send_email(to_email, "Password Reset Request", "password_reset_email.html", context)


def send_payment_confirmation_email(to_email):
    context = {
        'name': 'User',
        'amount': "$100.00",  # Replace with actual amount
        'transaction_id': "1234567890",  # Replace with actual transaction ID
    }
    send_email(to_email, "Payment Confirmation", "payment_confirmation_email.html", context)



if __name__ == "__main__":
    check_for_new_emails()
