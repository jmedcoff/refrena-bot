"""Role management commands and listeners."""
import discord
from discord.ext import commands
import logging
from config import Config

from utils.role_helpers import collect_reactions, add_missing_roles, remove_stale_roles

logger = logging.getLogger(__name__)

PRONOUN_CHANNEL_ID = Config.PRONOUN_CHANNEL_ID
PRONOUN_MESSAGE_ID = Config.PRONOUN_MESSAGE_ID

# Emoji to Role ID mapping - Replace with your actual role IDs
EMOJI_ROLE_MAP = {
    "💙": Config.PRONOUN_ROLE_HE,  # he/him role ID
    "🩷": Config.PRONOUN_ROLE_SHE,  # she/her role ID
    "💚": Config.PRONOUN_ROLE_THEY,  # they/them role ID
    "🧡": Config.PRONOUN_ROLE_ANY,  # any pronouns role ID
}


class Roles(commands.Cog):
    """Role management commands and listeners."""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_load(self):
        """Sync pronoun roles on cog load."""
        logger.info("Roles cog loaded, syncing pronoun roles...")
        if PRONOUN_MESSAGE_ID != 0:
            await self.sync_pronoun_roles()
        else:
            logger.warning("PRONOUN_MESSAGE_ID not found/configured, skipping sync")
    
    async def sync_pronoun_roles(self):
        """Sync roles based on current reactions - adds AND removes roles as needed."""
        try:
            message = await self._fetch_pronoun_message()
            if not message:
                return
            
            # Collect current reactions
            current_reactions = await collect_reactions(message, EMOJI_ROLE_MAP)
            
            # Add missing roles
            added_count = await add_missing_roles(message.guild, current_reactions, EMOJI_ROLE_MAP)
            
            # Remove stale roles
            removed_count = await remove_stale_roles(message.guild, current_reactions, EMOJI_ROLE_MAP)
            
            logger.info(f"Pronoun role sync complete. {added_count} roles added, {removed_count} roles removed.")
        
        except discord.NotFound:
            logger.error(f"Message {PRONOUN_MESSAGE_ID} not found")
        except discord.Forbidden:
            logger.error("Bot lacks permissions to manage roles or fetch message")
        except Exception as e:
            logger.error(f"Error syncing pronoun roles: {e}", exc_info=True)
    
    async def _fetch_pronoun_message(self) -> discord.Message | None:
        """Fetch the pronoun message. Returns None if not found."""
        channel = self.bot.get_channel(PRONOUN_CHANNEL_ID)
        if not channel:
            logger.error(f"Could not find channel {PRONOUN_CHANNEL_ID}")
            return None
        
        message = await channel.fetch_message(PRONOUN_MESSAGE_ID)
        if not message:
            logger.error(f"Could not find message {PRONOUN_MESSAGE_ID} in channel {PRONOUN_CHANNEL_ID}")
            return None
        
        return message
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Handle reaction additions for pronoun role assignment."""
        # Ignore reactions on other messages
        if payload.message_id != PRONOUN_MESSAGE_ID:
            return
        
        # Ignore bot reactions
        if payload.user_id == self.bot.user.id:
            return
        
        emoji_str = str(payload.emoji)
        
        # Ignore non-mapped emojis
        if emoji_str not in EMOJI_ROLE_MAP:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        member = guild.get_member(payload.user_id)
        if not member:
            return
        
        role = guild.get_role(EMOJI_ROLE_MAP[emoji_str])
        if not role:
            logger.warning(f"Role {EMOJI_ROLE_MAP[emoji_str]} not found for emoji {emoji_str}")
            return
        
        # Skip if member already has the role
        if role in member.roles:
            return
        
        try:
            await member.add_roles(role, reason=f"Pronoun role reaction: {emoji_str}")
            logger.info(f"Added {role.name} to {member.name}")
        except discord.Forbidden:
            logger.error(f"Missing permissions to add role {role.name}")
        except Exception as e:
            logger.error(f"Error adding role: {e}", exc_info=True)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Handle reaction removals for pronoun role removal."""
        if payload.message_id != PRONOUN_MESSAGE_ID:
            return
        
        emoji_str = str(payload.emoji)
        
        if emoji_str not in EMOJI_ROLE_MAP:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        member = guild.get_member(payload.user_id)
        if not member:
            return
        
        role = guild.get_role(EMOJI_ROLE_MAP[emoji_str])
        if not role:
            return
        
        if role not in member.roles:
            return
        
        try:
            await member.remove_roles(role, reason=f"Pronoun role reaction removed: {emoji_str}")
            logger.info(f"Removed {role.name} from {member.name}")
        except discord.Forbidden:
            logger.error(f"Missing permissions to remove role {role.name}")
        except Exception as e:
            logger.error(f"Error removing role: {e}", exc_info=True)
    
    @commands.command(name="sync_pronouns")
    @commands.has_permissions(administrator=True)
    async def sync_pronouns_command(self, ctx):
        """Manually trigger pronoun role sync (Admin only)."""
        await ctx.send("Syncing pronoun roles...")
        await self.sync_pronoun_roles()
        await ctx.send("Pronoun role sync complete!")


async def setup(bot):
    """Required function to load the cog."""
    await bot.add_cog(Roles(bot))