import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TEMP_FOLDER = os.getenv("TEMP_FOLDER", "temp")
    DEBUG = os.getenv("DEBUG", "True").lower() in ["true", "1", "yes"]