
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

IMAP_SERVER = os.getenv("IMAP_SERVER") 
IMAP_PORT = int(os.getenv("IMAP_PORT"))
EMAIL_ACCOUNT = SMTP_USER

