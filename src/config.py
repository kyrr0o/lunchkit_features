import os
from datetime import timedelta
from dotenv import load_dotenv
from distutils.util import strtobool
import cloudinary

load_dotenv()

class Config:
    # Basic Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    # SESSION_TYPE = 'filesystem'
    
    

    print("Loading GOOGLE_CLIENT_ID:", os.getenv('GOOGLE_CLIENT_ID'))
    
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    if not GOOGLE_CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID not found in environment variables")
    
        #cloudinary configuration
    cloud_config = cloudinary.config(
        secure=True)


    # Database configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.getenv('SECRET_KEY')

    PERMANENT_SESSION_LIFETIME_OWNER = timedelta(hours=15)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)
    SESSION_COOKIE_SECURE = False  
    DEBUG = os.getenv('FLASK_ENV') == 'development'

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = bool(strtobool(os.getenv('MAIL_USE_TLS')))
    MAIL_USE_SSL = bool(strtobool(os.getenv('MAIL_USE_SSL')))
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@lunchkit.com')
    
    