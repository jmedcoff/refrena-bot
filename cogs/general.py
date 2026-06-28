import discord
from discord.ext import commands
import logging
from config import Config

logger = logging.getLogger(__name__)

RULE_CHANNEL_ID = Config.RULE_CHANNEL_ID
RULE_MESSAGE_ID = Config.RULE_MESSAGE_ID

class General(commands.Cog):
    """General purpose commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    # When a user posts a message containing "!rule n", the bot will post rule number n from the rules message in the rules channel.
    @commands.command(name="rule", help="Get a specific rule by number. Usage: !rule <number>")
    async def rules(self, ctx, rule_number: int):
        """Fetch and display a specific rule from the rules message."""
        try:
            if not isinstance(rule_number, int) or rule_number < 1:
                logger.warning(f"Invalid rule number requested: {rule_number}")
                return
        
            channel = self.bot.get_channel(RULE_CHANNEL_ID)
            if not channel:
                logger.error(f"Rules channel with ID {RULE_CHANNEL_ID} not found")
                return
            
            message = await channel.fetch_message(RULE_MESSAGE_ID)
            if not message:
                logger.error(f"Rules message with ID {RULE_MESSAGE_ID} not found in channel {RULE_CHANNEL_ID}")
                return
            
            # The message format is "1. Rule one text\n explanation \n 2. Rule two text\n explanation \n ..."
            # but we only care about the number and the text, not the explanation. 
            # So we will split by lines, and then filter for lines that start with the rule number.
            # Make sure to ignore bold formatting (i.e., "**1. Rule one text**" should still match rule number 1).
            lines = message.content.splitlines()
            rule_lines = [line for line in lines if line.strip().lstrip("*").startswith(f"{rule_number}.")]
            
            # remove this later
            logger.debug(f"Rule lines found for rule {rule_number}: {rule_lines}")

            # include a ping "@admin"
            if rule_lines:
                await ctx.send(f"<@&{Config.ADMIN_ROLE_ID}>\n" + "\n".join(rule_lines))
            else:
                await ctx.send(f"Rule number {rule_number} not found.")
                logger.warning(f"Rule number {rule_number} not found in rules message.")
        
        except discord.NotFound:
            await ctx.send("Could not find the specified rule or channel.")
        except discord.Forbidden:
            logger.error("Bot lacks permissions to fetch the rules message or send messages in the channel")
        except Exception as e:
            logger.error(f"Error fetching rule: {e}")
    
    # TODO: Add general commands here (e.g. help, info, fun commands, etc.)

async def setup(bot):
    """Required function to load the cog."""
    await bot.add_cog(General(bot))
