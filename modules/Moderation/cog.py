import nextcord
from nextcord.ext import commands
import os
import datetime
import asyncio


class Moderation(commands.Cog, name="Moderation"):
    """Receives Moderation commands"""

    COG_EMOJI = "🛡️"

    def __init__(self, bot: commands.Bot):
        self.bot = bot    

    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True, administrator=True)
    async def purge(self, ctx, amount=6):
        """purges a user in the server"""
        await ctx.channel.purge(limit=amount)
        embed = nextcord.Embed(title=f"{amount} messages has been purged!", colour=nextcord.Colour.blue(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed) 
        
    @purge.error
    async def kick_error(self, error, ctx):
        if isinstance(error, error.MissingPermissions):
            await ctx.send(":redTick: You don't have permission to purge messages.")                             
                
    @commands.command(name='mute')
    @commands.has_permissions(manage_messages=True, administrator=True)
    async def mute(self, ctx, member: nextcord.Member, *, reason=None):
        """Mute a user from the server"""
        guild = ctx.guild
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        embed = nextcord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=nextcord.Colour.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.reply(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f"You have been muted from: {guild.name} Reason: {reason}")

    @mute.error
    async def kick_error(self, error, ctx):
        if isinstance(error, error.MissingPermissions):
            await ctx.send(":redTick: You don't have permission to mute members.")    


    @commands.command(name='unmute')
    @commands.has_permissions(manage_messages=True, administrator=True)
    async def unmute(self, ctx, member: nextcord.Member):
        """Unmute a user from the server"""
        mutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f"You have unmuted from: {ctx.guild.name}")
        embed = nextcord.Embed(title="Unmute", description=f"Unmuted {member.mention}", colour=nextcord.Colour.blue(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed)

    @unmute.error
    async def kick_error(self, error, ctx):
        if isinstance(error, error.MissingPermissions):
            await ctx.send(":redTick: You don't have permission to unmute members.")    

    @commands.command(name='kick')
    @commands.has_permissions(manage_messages=True, administrator=True)
    async def kick(self, ctx, member: nextcord.Member, reason="No Reason"):
        """kicks a user from the server"""
        if member == None:
            embed = nextcord.Embed(f"{ctx.message.author}, Please enter a valid user!")
            await ctx.reply(embed=embed)

        else:
            guild = ctx.guild
            embed = nextcord.Embed(title="Kicked!", description=f"{member.mention} has been kicked!!", colour=nextcord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Reason: ", value=reason, inline=False)
            await ctx.reply(embed=embed)
            await guild.kick(user=member)

    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, error.MissingPermissions):
            await ctx.send(":redTick: You don't have permission to kick members.")        

    @commands.command(name='ban')
    @commands.has_permissions(manage_messages=True, administrator=True)
    async def ban(self, ctx, member: nextcord.Member, reason="No Reason"):
        """Ban a user from the server"""
        if member == None:
            embed = nextcord.Embed(f"{ctx.message.author}, Please enter a valid user!")
            await ctx.reply(embed=embed)
        else:
            guild = ctx.guild
            embed = nextcord.Embed(title="Banned!", description=f"{member.mention} has been banned!", colour=nextcord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Reason: ", value=reason, inline=False)
            await ctx.reply(embed=embed)
            await guild.ban(user=member)

    @ban.error
    async def kick_error(self, error, ctx):
        if isinstance(error, error.MissingPermissions):
            await ctx.send(":redTick: You don't have permission to ban members.")        



    @commands.command(name='unban')
    @commands.has_permissions(manage_messages=True, administrator=True)
    async def unban(self, ctx, user: nextcord.User):
        """Unban a user from the server"""
        if user == None:
            embed = nextcord.Embed(f"{ctx.message.author}, Please enter a valid user!")
            await ctx.reply(embed=embed)

        else:
            guild = ctx.guild
            embed = nextcord.Embed(title="Unbanned!", description=f"{user.display_name} has been unbanned!", colour=nextcord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed)
            await guild.unban(user=user)

    @unban.error
    async def kick_error(self, error, ctx):
        if isinstance(error, error.MissingPermissions):
            await ctx.send(":redTick: You don't have permission to unban members.")             


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
