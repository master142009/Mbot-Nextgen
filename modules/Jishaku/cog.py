from nextcord.ext import commands

from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES

class CustomDebugCog(*OPTIONAL_FEATURES, *STANDARD_FEATURES):
    pass

def setup(bot: commands.Bot):
    bot.add_cog(CustomDebugCog(bot=bot))
