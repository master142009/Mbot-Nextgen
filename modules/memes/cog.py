from cgitb import text
from pydoc import describe
import nextcord
import requests
from nextcord.ext import commands
import aiohttp
import giphy_client
import random
from giphy_client.rest import ApiException

class Memes(commands.Cog, name="Memes"):
    """Receives Meme commands"""

    COG_EMOJI = "🐸"

    def __init__(self, bot: commands.Bot):
        self._bot = bot    

    @commands.command(aliases=["memes"])
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


    @commands.command(aliases=["c"])
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

    @commands.command(aliases=["d"])
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

    @commands.command(aliases=["giff", "g", "giphy"])
    async def gif(ctx,*,q="Smile"):

        api_key = "oROLhKkeAARPPfXuoJPm3uTzPsdf1d3B"
        api_instance = giphy_client.DefaultApi()

        try:

            api_responce = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_responce.data)
            giff = random.choice(lst)

            e = nextcord.Embed(title=q)
            e.set_image(url=f"https://media.giphy.com/media/{giff.id}/giphy.gif")

            await ctx.send(embed=e)

        except ApiException as r:
            print("Exception for the api")    



def setup(bot: commands.Bot):
    bot.add_cog(Memes(bot))
