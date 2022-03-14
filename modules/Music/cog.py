from unicodedata import name
import nextcord
from nextcord.ext import commands, activities

class MakeLinkBtn(nextcord.ui.view):
    def __init__(self, Link:str):
        super().__init__()
        self.add_item(nextcord.ui.Button(Label="Join Game!", url=f"{Link}"))

class Music(commands.Cog, name="Music"):
    """Recives Music commands"""

    COG_EMOJI = "🎵"

    def __init__(self, bot: commands.Bot):
        self._bot = bot 

    @commands.group(imvoke_without_commands = True)
    async def play(ctx):
        return

    @play.command()
    async def sketch(ctx, channel: nextcord.TextChannel = None):
        if channel == None:
            return await ctx.send("please specifly a channel type to join/create a game")

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.sketch)
        except nextcord.HTTPException:
            return ctx.send("please mention a voice channel to join/create a game")
        em = nextcord.Embed(title="Sketch Game", description=f"{ctx.author.mention} has been created a game in {channel.mention}")
        em.add_field(name="How to Play?", description="its like skribble.io but in a vc... someone draws something and everyone else has to guess what it is.")
        em.set_thumbnail(url="https://support.discord.com/hc/article_attachments/4503731144471/Discord_SketchHeads_Lobby.png")

        await ctx.send(embed=em)




def setup(bot):
    bot.add_cog(Music(bot))
