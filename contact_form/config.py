import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
MAIL_ENABLED = True  
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
