from cgitb import text
from pydoc import describe
import nextcord
import requests
from nextcord.ext import commands
import aiohttp

class Memes(commands.Cog, name="Memes"):
    """Receives Meme commands"""

    COG_EMOJI = "🐸"

    def __init__(self, bot: commands.Bot):
        self._bot = bot    

    @commands.command()
    async def reddit(self, ctx: commands.Context):
        """Sends Funny reddit posts"""
        async with ctx.channel.typing():
            r = requests.get("https://memes.blademaker.tv/api?lang=en")
            res = r.json()
            title = res["title"]
            ups = res["ups"]
            downs = res["downs"]
            sub = res["subreddit"]
            m = nextcord.Embed(title = f"{title}\n {sub}")
            m.set_image(url = res["image"])
            m.set_footer(text=f"👍 - {ups} 👎 - {downs}")
        await ctx.send(embed = m)


    @commands.command()
    async def cat(self, ctx: commands.Context):
        """Sends cute cat images"""
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    Embed = nextcord.Embed(title="Meow")
                    Embed.set_image(url=data['file'])
                    Embed.set_footer(text="http://random.cat/")
        await ctx.send(embed = Embed)

    @commands.command()
    async def dog(self, ctx: commands.Context):
        """Sends cute dog images"""
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    Embed = nextcord.Embed(title="Woof")
                    Embed.set_image(url=data['url'])
                    Embed.set_footer(text="https://random.dog/")
        await ctx.send(embed = Embed)



def setup(bot: commands.Bot):
    bot.add_cog(Memes(bot))
