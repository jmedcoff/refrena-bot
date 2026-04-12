import discord
from discord.ext import commands
from discord import app_commands
import logging
import psutil

logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    """Admin and infrastructure commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping")
    @commands.is_owner()
    async def ping(self, ctx):
        """Check latency."""
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f"Latency: {latency_ms}ms")
    
    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """Reload a cog (admin only). Usage: !reload <cog_name>"""
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Reloaded cog: {cog}")
            logger.info(f"Reloaded cog: {cog} (requested by {ctx.author})")
        except Exception as e:
            await ctx.send(f"Failed to reload cog: {cog}\nError: {e}")
            logger.error(f"Failed to reload cog: {cog} (requested by {ctx.author}): {e}")
    
    @commands.command(name="status")
    @commands.is_owner()
    async def status(self, ctx):
        """Check bot status (admin only)."""
        uptime = discord.utils.format_dt(self.bot.user.created_at, style='R')
        await ctx.send(f"Uptime: {uptime}\nLatency: {round(self.bot.latency * 1000)}ms\nCogs loaded: {list(self.bot.cogs.keys())}\nServer memory: {psutil.virtual_memory().percent}%")


async def setup(bot):
    """Required function to load the cog."""
    await bot.add_cog(Admin(bot))
