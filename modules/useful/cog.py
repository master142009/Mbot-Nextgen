from unicodedata import name
from discord import User
from nextcord import BotIntegration, Guild, client
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import BucketType, cooldown
import datetime
import time
import json
import asyncio
import psutil
import os

from psutil import users

from.help_command import MyHelpCommand

class Useful(commands.Cog, name="Useful"):
    """Shows Useful commands"""

    COG_EMOJI = "❔"

    def __init__(self, bot: commands.Bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self
        self.bot = bot
        

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


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
        e.timestamp = datetime.datetime.utcnow()
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
        e.timestamp = datetime.datetime.utcnow()
        e.set_footer(
            text=f"Ping test by {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}")
        await ctx.send(embed=e)

    @commands.command(aliases=["si", "serverinfo"])
    async def server(self, ctx):
        """ Info related to server"""
        own = str(ctx.guild.owner)
        tim = str(ctx.guild.created_at)
        txt = len(ctx.guild.text_channels)
        vc = len(ctx.guild.voice_channels)
        embed = nextcord.Embed(
            timestamp=ctx.message.created_at,
            title="Server Info",
            color=0xFF0000,
        )
        embed.add_field(name=":ballot_box: Name", value=f"{ctx.guild}")
        embed.add_field(name=":crown: Owner", value=own)
        embed.add_field(
            name="Members",
            value=f"{ctx.guild.member_count}",
        )
        embed.add_field(name=":calendar: Created At", value=f"{tim[0:11]}")
        embed.add_field(
            name="Text Channels", value=f"{txt}"
        )
        embed.add_field(
            name="Voice Channels", value=f"{vc}"
        )
        embed.add_field(
            name="Prefix", value=f"`m?`", inline=False
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}"
        )

        embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["bi", "about"])
    async def bot(self, ctx):
        """ Info related to bot"""
        ser = len(self.bot.guilds)
        mem = len(self.bot.users)
        embed = nextcord.Embed(
            timestamp=ctx.message.created_at, title=":robot:  Bot Info", color=0xFF0000
        )
        embed.set_thumbnail(url="https://i.imgur.com/61Bromb.png")
        embed.add_field(
            name="Helping", value=f"{ser} servers"
        )
        embed.add_field(
            name="Serving", value=f"{mem} members"
        )
        embed.add_field(name="Prefix", value=f"`m?`")
        embed.add_field(
            name="Support Server",
            value="[Comming soon](https://....)",
        )
        embed.add_field(
            name="Add Me",
            value="[Click Here to Add Me](https://discord.com/api/oauth2/authorize?client_id=888675856497643561&permissions=8&scope=bot)",
        )
        embed.add_field(
            name="Website",
            value="[Comming soon](https://....)",
        )
        embed.add_field(
            name="Made By", value="Master v#2926"
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["ui", "userinfo"])
    async def user(self, ctx, member: nextcord.Member = None):
        """ Info related to a user"""
        if member == None:
            member = ctx.message.author
        else:
            pass
        c = str(member.created_at)[0:11]
        j = str(member.joined_at)[0:11]
        embed = nextcord.Embed(
            timestamp=ctx.message.created_at,
            title="User Info",
            color=0xFF0000,
        )
        embed.set_thumbnail(url=member.author.avatar.url)
        embed.add_field(name=":name_badge: Name", value=f"{member.name}")
        embed.add_field(
            name="Nickname", value=f"{member.nick}"
        )
        embed.add_field(name=":credit_card: Id", value=f"{member.id}")
        embed.add_field(name=":flower_playing_cards: Joined Discord", value=f"{c}")
        embed.add_field(
            name="Joined Server", value=f"{j}"
        )
        embed.add_field(
            name="Highest Role",
            value=f"{member.top_role.mention}",
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}"
        )
        await ctx.send(embed=embed)    

def setup(bot: commands.Bot):
    bot.add_cog(Useful(bot))
