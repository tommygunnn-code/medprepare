import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TEMP_FOLDER = os.getenv("TEMP_FOLDER", "temp")
    DEBUG = os.getenv("DEBUG", "True").lower() in ["true", "1", "yes"]
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')