"""Configuration management for the Discord bot."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot configuration from environment variables."""
    
    # Required
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
    # Optional
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is required in .env file")
        
        return True
