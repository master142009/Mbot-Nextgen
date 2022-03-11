import random
from nextcord.ext import commands
import nextcord
import asyncio

class Music(commands.Cog, name="Music"):
    """Recives Game information to play."""

    COG_EMOJI = "🎮"

    def __init__(self, bot: commands.Bot):
        self._bot = bot 

    

def setup(bot):
    bot.add_cog(Music(bot))
