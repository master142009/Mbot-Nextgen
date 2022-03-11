from unicodedata import name
from nextcord import client
import nextcord
from nextcord.ext import commands
import time
import json
import asyncio


class Ping(commands.Cog, name="Ping"):
    """Receives Ping commands"""

    COG_EMOJI = "📒"

    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Sends ping of the bot"""
        before = time.monotonic()
        message = await ctx.send("Testing...")
        ping = (time.monotonic() - before) * 1000
        e = nextcord.Embed(title="Connection", colour=909999)
        e.set_author(name=f"{ctx.author.name}",
                    icon_url=f"{ctx.author.avatar.url}")
        e.add_field(name="Ping", value=str(f"`{int(ping)}ms`"), inline=False)
        e.set_footer(
            text=f"Ping test by {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}")
        await ctx.send(embed=e)

        

    @commands.command(pass_context=True)
    async def mping(self, ctx):
        """Sends multiple pings of the bot"""
        channel = ctx.message.channel
        try:
            t1 = time.perf_counter()
            await ctx.send("This Message is for test to check pings!")
            ta = t1
            t2 = time.perf_counter()
            await ctx.send("This Message is for test to check pings!")
            tb = t2
            ra = round((tb - ta) * 1000)
        finally:
            pass
        try:
            t1a = time.perf_counter()
            await ctx.send("This Message is for test to check pings!")
            ta1 = t1a
            t2a = time.perf_counter()
            await ctx.send("This Message is for test to check pings!")
            tb1 = t2a
            ra1 = round((tb1 - ta1) * 1000)
        finally:
            pass
        try:
            t1b = time.perf_counter()
            await ctx.send("This Message is for test to check pings!")
            ta2 = t1b
            t2b = time.perf_counter()
            await ctx.send("This Message is for test to check pings!")
            tb2 = t2b
            ra2 = round((tb2 - ta2) * 1000)
        finally:
            pass
        try:
            t1c = time.perf_counter()
            await ctx.send("This Message is for test to check pings!")
            ta3 = t1c

            t2c = time.perf_counter()

            tb3 = t2c

            ra3 = round((tb3 - ta3) * 1000)
        finally:
            pass
        try:
            t1d = time.perf_counter()
            await ctx.send("This Message is for test to check pings!")
            ta4 = t1d

            t2d = time.perf_counter()
            tb4 = t2d

            ra4 = round((tb4 - ta4) * 1000)
        finally:
            pass

        e = nextcord.Embed(title="Connection", colour=909999)
        e.set_author(name=f"{ctx.author.name}",
                    icon_url=f"{ctx.author.avatar.url}")
        e.add_field(name='Ping 1', value=str(f"`{int(ra)}ms`"), inline=False)
        e.add_field(name='Ping 2', value=str(f"`{int(ra2)}ms`"), inline=False)
        e.add_field(name='Ping 3', value=str(f"`{int(ra3)}ms`"), inline=False)
        e.add_field(name='Ping 4', value=str(f"`{int(ra4)}ms`"), inline=False)
        e.set_footer(
            text=f"Ping test by {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}")
        await ctx.send(embed=e) 

    

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
