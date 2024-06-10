import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'polling_db'
    DB_USER = os.environ.get('DB_USER') or 'your_username'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'your_password'
