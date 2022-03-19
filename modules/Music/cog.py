from nextcord import ClientException
from nextcord.ext import commands

class music(commands.Cog, name="music"):
    """Recives Music commands"""

    COG_EMOJI = "🎵"

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot 
        
        



def setup(bot):
    bot.add_cog(music(bot))
