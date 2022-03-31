from cgitb import text
from pydoc import describe
import nextcord
import requests
from nextcord.ext import commands
import aiohttp
import giphy_client
import random
from giphy_client.rest import ApiException
import requests
from aiohttp import request

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

    @commands.command()
    async def gif(ctx,*,q="random"):
        """Sends gif images."""
        api_key="Fqi6cJfMpTPkePMA34e6sL4Y39otSJl9"
        api_instance = giphy_client.DefaultApi()

        try: 
            
            api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_response.data)
            giff = random.choice(lst)

            emb = nextcord.Embed(title=q)
            emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

            await ctx.channel.send(embed=emb)
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

    @commands.command(aliases=["dadjokes", "dj"])
    async def dadjoke(ctx):

        url = "https://dad-jokes.p.rapidapi.com/random/joke"

        async with request("GET", url, headers={}) as responce:
            if responce.status == 200:
                data = await responce.json()
                await ctx.send(f"**{data['setup']}**\n\n||{data['punchline']}||")
            else:
                await ctx.send(f"{responce.status}")                



def setup(bot: commands.Bot):
    bot.add_cog(Memes(bot))
