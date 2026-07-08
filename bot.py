"""Main Discord bot entry point."""
import random

import discord
from discord.ext import commands
import logging
import asyncio
from pathlib import Path

from config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RefrenaBot(commands.Bot):
    """Custom bot class with additional functionality."""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=Config.COMMAND_PREFIX,
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )
    
    async def setup_hook(self):
        """Called when the bot is starting up - load cogs here."""
        logger.info("Loading cogs...")
        
        # Load all cogs from the cogs directory
        cogs_path = Path(__file__).parent / "cogs"
        if cogs_path.exists():
            for cog_file in cogs_path.glob("*.py"):
                if cog_file.stem != "__init__":
                    try:
                        await self.load_extension(f"cogs.{cog_file.stem}")
                        logger.info(f"Loaded cog: {cog_file.stem}")
                    except Exception as e:
                        logger.error(f"Failed to load cog {cog_file.stem}: {e}")
    
    async def on_ready(self):
        """Called on successful connection to Discord."""
        logger.info(f'Bot is ready! Logged in as {self.user} (ID: {self.user.id})')
        logger.info(f'Connected to {len(self.guilds)} guilds')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="Violet Pulse SPA"
            )
        )
    
    async def on_command_error(self, ctx, error):
        """Global error handler for commands."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore unknown commands
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: {error.param.name}")
            return
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"❌ This command is on cooldown. Try again in {error.retry_after:.1f}s.")
            return

        # Log unexpected errors
        trace_identifier = random.randint(1000, 9999)  # Simple trace ID for correlating logs
        logger.error(f"Error in command {ctx.command} (Trace ID: {trace_identifier}): {error}", exc_info=error)
        await ctx.send(f"❌ An error occurred while processing the command. ({trace_identifier})")


async def main():
    """Main entry point for the bot."""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    
    # Create and run the bot
    bot = RefrenaBot()
    
    try:
        async with bot:
            await bot.start(Config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
