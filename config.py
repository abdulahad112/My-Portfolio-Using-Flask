import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # App secret
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f4c2b1d3a6e4f0b72c9d8e1f7a3b5c6d'
    
    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail (Gmail example)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes')
    
    # Email credentials
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'gokuahad11@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'gcqqvhdepvfewoak'
    
    # Default sender and admin email
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'gokuahad11@gmail.com'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'gokuahad11@gmail.com'