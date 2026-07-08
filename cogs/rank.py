"""Rank assignment commands and listeners."""
import discord
from discord.ext import commands
import logging
from config import Config

from utils.rank_role_helpers import get_rank_congrats_message

logger = logging.getLogger(__name__)

rank_role_map = {
    # SP ranks
    "sp7kyu": Config.RANK_ROLE_SP7KYU,
    "sp6kyu": Config.RANK_ROLE_SP6KYU,
    "sp5kyu": Config.RANK_ROLE_SP5KYU,
    "sp4kyu": Config.RANK_ROLE_SP4KYU,
    "sp3kyu": Config.RANK_ROLE_SP3KYU,
    "sp2kyu": Config.RANK_ROLE_SP2KYU,
    "sp1kyu": Config.RANK_ROLE_SP1KYU,
    "sp1dan": Config.RANK_ROLE_SP1DAN,
    "sp2dan": Config.RANK_ROLE_SP2DAN,
    "sp3dan": Config.RANK_ROLE_SP3DAN,
    "sp4dan": Config.RANK_ROLE_SP4DAN,
    "sp5dan": Config.RANK_ROLE_SP5DAN,
    "sp6dan": Config.RANK_ROLE_SP6DAN,
    "sp7dan": Config.RANK_ROLE_SP7DAN,
    "sp8dan": Config.RANK_ROLE_SP8DAN,
    "sp9dan": Config.RANK_ROLE_SP9DAN,
    "sp10dan": Config.RANK_ROLE_SP10DAN,
    "spchuuden": Config.RANK_ROLE_SPCHUUDEN,
    "spkaiden": Config.RANK_ROLE_SPKAIDEN,
    # DP ranks
    "dp7kyu": Config.RANK_ROLE_DP7KYU,
    "dp6kyu": Config.RANK_ROLE_DP6KYU,
    "dp5kyu": Config.RANK_ROLE_DP5KYU,
    "dp4kyu": Config.RANK_ROLE_DP4KYU,
    "dp3kyu": Config.RANK_ROLE_DP3KYU,
    "dp2kyu": Config.RANK_ROLE_DP2KYU,
    "dp1kyu": Config.RANK_ROLE_DP1KYU,
    "dp1dan": Config.RANK_ROLE_DP1DAN,
    "dp2dan": Config.RANK_ROLE_DP2DAN,
    "dp3dan": Config.RANK_ROLE_DP3DAN,
    "dp4dan": Config.RANK_ROLE_DP4DAN,
    "dp5dan": Config.RANK_ROLE_DP5DAN,
    "dp6dan": Config.RANK_ROLE_DP6DAN,
    "dp7dan": Config.RANK_ROLE_DP7DAN,
    "dp8dan": Config.RANK_ROLE_DP8DAN,
    "dp9dan": Config.RANK_ROLE_DP9DAN,
    "dp10dan": Config.RANK_ROLE_DP10DAN,
    "dpchuuden": Config.RANK_ROLE_DPCHUUDEN,
    "dpkaiden": Config.RANK_ROLE_DPKAIDEN
}

class RankAssignment(commands.Cog):
    """Rank assignment commands and listeners."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rank", help="Assign a rank role based on your rank. Usage: !rank <rank>")
    @commands.cooldown(2, 15, commands.BucketType.user)
    async def assign_rank(self, ctx, rank: str):
        """Assign a rank role to the user based on the provided rank string."""
        rank = rank.lower()
        # check format
        if not (rank.startswith("sp") or rank.startswith("dp")) or not (rank.endswith("kyu") or rank.endswith("dan") or rank.endswith("chuuden") or rank.endswith("kaiden")):
            logger.warning(f"Invalid rank format: {rank} from user {ctx.author} in guild {ctx.guild}")
            await ctx.send("Usage: !rank <rank>. Example: !rank sp1dan or !rank dp7kyu. Valid ranks are sp/dp + 7kyu-1kyu, 1dan-10dan, chuuden, kaiden.")
            return
        
        if rank not in rank_role_map:
            logger.warning(f"Rank not recognized: {rank} from user {ctx.author} in guild {ctx.guild}")
            await ctx.send(f"Rank not recognized: {rank}", allowed_mentions=discord.AllowedMentions.none())
            return

        role_id = rank_role_map[rank]
        role = ctx.guild.get_role(role_id)
        if not role:
            logger.warning(f"Role not found for rank: {rank} in guild {ctx.guild}")
            await ctx.send(f"Rank not recognized: {rank}", allowed_mentions=discord.AllowedMentions.none())
            return
        
        # if the rank requested is the same as the user's current rank role, remove it instead
        if role in ctx.author.roles:
            try:
                await ctx.author.remove_roles(role, reason=f"Refrena: removed rank role: {rank}")
                await ctx.send(f"Removed rank role: {role.name}")
                logger.info(f"Removed rank role {role.name} from {ctx.author.name}")
            except discord.Forbidden:
                logger.error(f"Missing permissions to remove role {role.name} from {ctx.author.name}")
            except Exception as e:
                logger.error(f"Error removing rank role: {e}", exc_info=True)
            return
        
        # if the user already has a role matching the playstyle (SP or DP), remove it before adding the new role
        playstyle_prefix = rank[:2]  # "sp" or "dp"
        for r in ctx.author.roles:
            if r.id in rank_role_map.values() and r.name.lower().startswith(playstyle_prefix):
                try:
                    await ctx.author.remove_roles(r, reason=f"Refrena: removing old rank ({r.name}) role while assigning new rank: {rank}")
                    logger.info(f"Removed old rank role {r.name} from {ctx.author.name}")
                except discord.Forbidden:
                    logger.error(f"Missing permissions to remove role {r.name} from {ctx.author.name}")
                except Exception as e:
                    logger.error(f"Error removing old rank role: {e}", exc_info=True)
        
        try:
            await ctx.author.add_roles(role, reason=f"Refrena: assigned rank role: {rank}")
            await ctx.send(get_rank_congrats_message(ctx.author.mention, rank))
        except discord.Forbidden:
            logger.error(f"Missing permissions to assign role {role.name} to {ctx.author.name}")
        except Exception as e:
            logger.error(f"Error assigning rank role: {e}", exc_info=True)

async def setup(bot):
    """Required function to load the cog."""
    await bot.add_cog(RankAssignment(bot))