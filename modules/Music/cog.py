from unicodedata import name
import nextcord
from nextcord.ext import commands, activities

class Music(commands.Cog, name="Music"):
    """Recives Music commands"""

    COG_EMOJI = "🎵"

    def __init__(self, bot: commands.Bot):
        self._bot = bot 

    



def setup(bot):
    bot.add_cog(Music(bot))
