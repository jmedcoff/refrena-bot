"""Helper functions for role management operations."""
import discord
import logging

logger = logging.getLogger(__name__)


async def get_or_fetch_member(guild: discord.Guild, user_id: int) -> discord.Member | None:
    """Return a Member from cache, falling back to a REST fetch if not cached."""
    member = guild.get_member(user_id)
    if member:
        return member
    try:
        return await guild.fetch_member(user_id)
    except discord.NotFound:
        return None
    except discord.HTTPException as e:
        logger.warning(f"Could not fetch member {user_id} from guild {guild.id}: {e}")
        return None


async def collect_reactions(message: discord.Message, emoji_filter: dict) -> set[tuple[int, str]]:
    """
    Collect all reactions from a message that match the emoji filter.
    
    Args:
        message: The Discord message to collect reactions from
        emoji_filter: Dict of emoji strings to filter by (e.g., EMOJI_ROLE_MAP)
    
    Returns:
        Set of (user_id, emoji_str) tuples for non-bot users
    """
    reactions = set()
    
    for reaction in message.reactions:
        emoji_str = str(reaction.emoji)
        if emoji_str not in emoji_filter:
            continue
        
        async for user in reaction.users():
            if not user.bot:
                reactions.add((user.id, emoji_str))
    
    return reactions


async def add_missing_roles(guild: discord.Guild, reactions: set[tuple[int, str]], 
                           emoji_role_map: dict) -> int:
    """
    Add roles to users based on their reactions.
    
    Args:
        guild: The Discord guild
        reactions: Set of (user_id, emoji_str) tuples
        emoji_role_map: Mapping of emoji strings to role IDs
    
    Returns:
        Number of roles added
    """
    added_count = 0
    
    for user_id, emoji_str in reactions:
        role_id = emoji_role_map[emoji_str]
        role = guild.get_role(role_id)
        
        if not role:
            logger.warning(f"Role {role_id} not found for emoji {emoji_str}")
            continue
        
        member = await get_or_fetch_member(guild, user_id)
        if not member:
            continue
        
        if role not in member.roles:
            try:
                await member.add_roles(role, reason="RefrenaBot: Pronoun role sync")
                added_count += 1
                logger.info(f"Added {role.name} to {member.name}")
            except discord.Forbidden:
                logger.error(f"Missing permissions to add {role.name} to {member.name}")
            except discord.HTTPException as e:
                logger.error(f"Failed to add {role.name} to {member.name}: {e}")
    
    return added_count


async def remove_stale_roles(guild: discord.Guild, current_reactions: set[tuple[int, str]], 
                            emoji_role_map: dict) -> int:
    """
    Remove roles from users who no longer have the corresponding reaction.
    
    Args:
        guild: The Discord guild
        current_reactions: Set of (user_id, emoji_str) tuples from current reactions
        emoji_role_map: Mapping of emoji strings to role IDs
    
    Returns:
        Number of roles removed
    """
    removed_count = 0
    
    for emoji_str, role_id in emoji_role_map.items():
        role = guild.get_role(role_id)
        if not role:
            continue
        
        # Check all members with this role
        for member in role.members:
            # If they don't have the corresponding reaction, remove the role
            if (member.id, emoji_str) not in current_reactions:
                try:
                    await member.remove_roles(role, reason="RefrenaBot: Pronoun role sync - reaction removed")
                    removed_count += 1
                    logger.info(f"Removed {role.name} from {member.name}")
                except discord.Forbidden:
                    logger.error(f"Missing permissions to remove {role.name} from {member.name}")
                except discord.HTTPException as e:
                    logger.error(f"Failed to remove {role.name} from {member.name}: {e}")
    
    return removed_count
