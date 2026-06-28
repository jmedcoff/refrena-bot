"""Configuration management for the Discord bot."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot configuration from environment variables."""
    
    # Required
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))

    PRONOUN_CHANNEL_ID = int(os.getenv("PRONOUN_CHANNEL_ID"))
    PRONOUN_MESSAGE_ID = int(os.getenv("PRONOUN_MESSAGE_ID"))

    PRONOUN_ROLE_SHE = int(os.getenv("PRONOUN_ROLE_SHE"))
    PRONOUN_ROLE_THEY = int(os.getenv("PRONOUN_ROLE_THEY"))
    PRONOUN_ROLE_ANY = int(os.getenv("PRONOUN_ROLE_ANY"))
    PRONOUN_ROLE_HE = int(os.getenv("PRONOUN_ROLE_HE"))

    RULE_CHANNEL_ID = int(os.getenv("RULE_CHANNEL_ID"))
    RULE_MESSAGE_ID = int(os.getenv("RULE_MESSAGE_ID"))
    
    # Optional
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is required in .env file")
        if not cls.PRONOUN_CHANNEL_ID:
            raise ValueError("PRONOUN_CHANNEL_ID is required in .env file")
        if not cls.PRONOUN_MESSAGE_ID:
            raise ValueError("PRONOUN_MESSAGE_ID is required in .env file")
        if not cls.PRONOUN_ROLE_SHE or not cls.PRONOUN_ROLE_THEY or not cls.PRONOUN_ROLE_ANY or not cls.PRONOUN_ROLE_HE:
            raise ValueError("All pronoun role IDs (SHE, THEY, ANY, HE) are required in .env file")
        if not cls.RULE_CHANNEL_ID:
            raise ValueError("RULE_CHANNEL_ID is required in .env file")
        if not cls.RULE_MESSAGE_ID:
            raise ValueError("RULE_MESSAGE_ID is required in .env file")
        
        return True
