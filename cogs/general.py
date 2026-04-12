import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)


class General(commands.Cog):
    """General purpose commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    # TODO: Add general commands here (e.g. help, info, fun commands, etc.)

async def setup(bot):
    """Required function to load the cog."""
    await bot.add_cog(General(bot))
