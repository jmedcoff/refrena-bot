"""Configuration management for the Discord bot."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot configuration from environment variables."""
    
    # Required
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID") or 0)

    PRONOUN_CHANNEL_ID = int(os.getenv("PRONOUN_CHANNEL_ID") or 0)
    PRONOUN_MESSAGE_ID = int(os.getenv("PRONOUN_MESSAGE_ID") or 0)

    PRONOUN_ROLE_SHE = int(os.getenv("PRONOUN_ROLE_SHE") or 0)
    PRONOUN_ROLE_THEY = int(os.getenv("PRONOUN_ROLE_THEY") or 0)
    PRONOUN_ROLE_ANY = int(os.getenv("PRONOUN_ROLE_ANY") or 0)
    PRONOUN_ROLE_HE = int(os.getenv("PRONOUN_ROLE_HE") or 0)

    RULE_CHANNEL_ID = int(os.getenv("RULE_CHANNEL_ID") or 0)
    RULE_MESSAGE_ID = int(os.getenv("RULE_MESSAGE_ID") or 0)
    
    # Optional
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
    
    RANK_ROLE_SP7KYU = int(os.getenv("RANK_ROLE_SP7KYU") or 0)
    RANK_ROLE_SP6KYU = int(os.getenv("RANK_ROLE_SP6KYU") or 0)
    RANK_ROLE_SP5KYU = int(os.getenv("RANK_ROLE_SP5KYU") or 0)
    RANK_ROLE_SP4KYU = int(os.getenv("RANK_ROLE_SP4KYU") or 0)
    RANK_ROLE_SP3KYU = int(os.getenv("RANK_ROLE_SP3KYU") or 0)
    RANK_ROLE_SP2KYU = int(os.getenv("RANK_ROLE_SP2KYU") or 0)
    RANK_ROLE_SP1KYU = int(os.getenv("RANK_ROLE_SP1KYU") or 0)
    RANK_ROLE_SP1DAN = int(os.getenv("RANK_ROLE_SP1DAN") or 0)
    RANK_ROLE_SP2DAN = int(os.getenv("RANK_ROLE_SP2DAN") or 0)
    RANK_ROLE_SP3DAN = int(os.getenv("RANK_ROLE_SP3DAN") or 0)
    RANK_ROLE_SP4DAN = int(os.getenv("RANK_ROLE_SP4DAN") or 0)
    RANK_ROLE_SP5DAN = int(os.getenv("RANK_ROLE_SP5DAN") or 0)
    RANK_ROLE_SP6DAN = int(os.getenv("RANK_ROLE_SP6DAN") or 0)
    RANK_ROLE_SP7DAN = int(os.getenv("RANK_ROLE_SP7DAN") or 0)
    RANK_ROLE_SP8DAN = int(os.getenv("RANK_ROLE_SP8DAN") or 0)
    RANK_ROLE_SP9DAN = int(os.getenv("RANK_ROLE_SP9DAN") or 0)
    RANK_ROLE_SP10DAN = int(os.getenv("RANK_ROLE_SP10DAN") or 0)
    RANK_ROLE_SPCHUUDEN = int(os.getenv("RANK_ROLE_SPCHUUDEN") or 0)
    RANK_ROLE_SPKAIDEN = int(os.getenv("RANK_ROLE_SPKAIDEN") or 0)
    
    RANK_ROLE_DP7KYU = int(os.getenv("RANK_ROLE_DP7KYU") or 0)
    RANK_ROLE_DP6KYU = int(os.getenv("RANK_ROLE_DP6KYU") or 0)
    RANK_ROLE_DP5KYU = int(os.getenv("RANK_ROLE_DP5KYU") or 0)
    RANK_ROLE_DP4KYU = int(os.getenv("RANK_ROLE_DP4KYU") or 0)
    RANK_ROLE_DP3KYU = int(os.getenv("RANK_ROLE_DP3KYU") or 0)
    RANK_ROLE_DP2KYU = int(os.getenv("RANK_ROLE_DP2KYU") or 0)
    RANK_ROLE_DP1KYU = int(os.getenv("RANK_ROLE_DP1KYU") or 0)
    RANK_ROLE_DP1DAN = int(os.getenv("RANK_ROLE_DP1DAN") or 0)
    RANK_ROLE_DP2DAN = int(os.getenv("RANK_ROLE_DP2DAN") or 0)
    RANK_ROLE_DP3DAN = int(os.getenv("RANK_ROLE_DP3DAN") or 0)
    RANK_ROLE_DP4DAN = int(os.getenv("RANK_ROLE_DP4DAN") or 0)
    RANK_ROLE_DP5DAN = int(os.getenv("RANK_ROLE_DP5DAN") or 0)
    RANK_ROLE_DP6DAN = int(os.getenv("RANK_ROLE_DP6DAN") or 0)
    RANK_ROLE_DP7DAN = int(os.getenv("RANK_ROLE_DP7DAN") or 0)
    RANK_ROLE_DP8DAN = int(os.getenv("RANK_ROLE_DP8DAN") or 0)
    RANK_ROLE_DP9DAN = int(os.getenv("RANK_ROLE_DP9DAN") or 0)
    RANK_ROLE_DP10DAN = int(os.getenv("RANK_ROLE_DP10DAN") or 0)
    RANK_ROLE_DPCHUUDEN = int(os.getenv("RANK_ROLE_DPCHUUDEN") or 0)
    RANK_ROLE_DPKAIDEN = int(os.getenv("RANK_ROLE_DPKAIDEN") or 0)
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is required in .env file")
        if not cls.ADMIN_ROLE_ID:
            raise ValueError("ADMIN_ROLE_ID is required in .env file")
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
