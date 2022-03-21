import os
import nextcord
import psutil
from nextcord.ext import commands
from nextcord.ext.commands import BucketType, cooldown
import motor.motor_asyncio
import nest_asyncio
import json
import random

nest_asyncio.apply()

mongo_url = "mongodb+srv://MasonmMasonn:Masonn14@galaxies.b117q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
ecomoney = cluster["eco"]["money"]

class Economy(commands.Cog, name="Economy"):
    """ Commands related to economy"""

    COG_EMOJI = "📉"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Eco Cog Loaded Succesfully")

    async def open_account(self, id : int):
            newuser = {"id": id, "wallet": 10000, "bank": 100}
            # wallet = current money, bank = money in bank
            await ecomoney.insert_one(newuser)

    async def update_wallet(self, id : int, wallet : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"wallet": wallet}})

    async def update_bank(self, id : int, bank : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"bank": bank}})


    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: nextcord.Member = None):
        """ Check your balance"""
        if member is None:
            member = ctx.message.author
        try:
            bal = await ecomoney.find_one({"id": member.id})
            if bal is None:
                await self.open_account(member.id)
                bal = await ecomoney.find_one({"id": member.id})
            embed = nextcord.Embed(
                timestamp=ctx.message.created_at,
                title=f"{member}'s Balance",
                color=0xFF0000,
            )
            embed.add_field(
                name="Wallet",
                value=f"<:minecoin:955431748081164308>{bal['wallet']}",
            )
            embed.add_field(
                name="Bank",
                value=f"<:minecoin:955431748081164308>{bal['bank']}",
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}"
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send('An error occured')    

    @commands.command(aliases=["wd"])
    async def withdraw(self, ctx, amount: int):
        """ Withdraw money from your bank"""
        user = ctx.message.author
        try:
            bal = await ecomoney.find_one({"id": user.id})
            if bal is None:
                await self.open_account(user.id)
                bal = await ecomoney.find_one({"id": user.id})
            if amount > bal['bank']:
                await ecomoney.update_one({"id": user.id}, {"$inc": {"wallet": +amount, "bank": -amount}})
                await ctx.send(f'You have withdrawn <:minecoin:955431748081164308>{amount}')
            elif amount <= 0:
                await ctx.send('You cannot withdraw 0 or less')
            else:
                await ctx.send('You do not have enough money to withdraw that much')
        except Exception:
            await ctx.send('An error occured')

    @commands.command(aliases=["dp"])
    async def deposit(self, ctx, amount: int):
        """ Deposit money to your bank"""
        user = ctx.message.author
        try:
            bal = await ecomoney.find_one({"id": user.id})
            if bal is None:
                await self.open_account(user.id)
                bal = await ecomoney.find_one({"id": user.id})
            if amount > bal['wallet']:
                await ecomoney.update_one({"id": user.id}, {"$inc": {"wallet": -amount, "bank": +amount}})
                await ctx.send(f'You have deposited <:minecoin:955431748081164308>{amount}')
            elif amount <= 0:
                await ctx.send('You cannot deposit 0 or less')
            else:
                await ctx.send('You do not have enough money to deposit that much')
        except Exception:
            await ctx.send('An error occured')

    @commands.command()
    async def rob(self, ctx, user: nextcord.Member = None):
        """ Rob someone"""
        if user is None or user.id == ctx.author.id:
            await ctx.send('Trying to rob yourself?')
        else:
            try:
                user_bal = await ecomoney.find_one({"id": user.id})
                member_bal = await ecomoney.find_one({"id": ctx.author.id})
                if user_bal is None:
                    await self.open_account(user.id)
                    user_bal = await ecomoney.find_one({"id": user.id})
                if member_bal is None:
                    await self.open_account(ctx.author.id)
                    member_bal = await ecomoney.find_one({"id": ctx.author.id})
                mem_bank = member_bal["bank"]
                user_bank = user_bal["bank"]
                if mem_bank < 100:
                    await ctx.send('You do not have enough money to rob someone')
                elif mem_bank >= 100:
                    if user_bank < 100:
                        await ctx.send('User do not have enough money to get robbed ;-;')
                    elif user_bank >= 100:
                        num = random.randint(1, 100)
                        f_mem = mem_bank + num
                        f_user = user_bank - num
                        await self.update_bank(ctx.author.id, f_mem)
                        await self.update_bank(user.id, f_user)
                        await ctx.send('You have robbed <:minecoin:955431748081164308>{num} from {user}'.format(num=num, user=user))


            except Exception:
                await ctx.send('An error occured')

    # send money to another user
    @commands.command()
    async def send(self, ctx, user: nextcord.Member, amount: int):
        """ Send money to another user"""
        try:
            user_bal = await ecomoney.find_one({"id": user.id})
            member_bal = await ecomoney.find_one({"id": ctx.author.id})
            if user_bal is None:
                await self.open_account(user.id)
                user_bal = await ecomoney.find_one({"id": user.id})
            if member_bal is None:
                await self.open_account(ctx.author.id)
                member_bal = await ecomoney.find_one({"id": ctx.author.id})
            mem_bank = member_bal["bank"]
            user_bank = user_bal["bank"]
            if amount > mem_bank or amount > 20000:
                await ctx.send('You do not have enough money to send that much or amount too much')
            elif amount <= 0:
                await ctx.send('You cannot send 0 or less')
            else:
                await ecomoney.update_one({"id": ctx.author.id}, {"$inc": {"bank": -amount}})
                await ecomoney.update_one({"id": user.id}, {"$inc": {"bank": +amount}})
                await ctx.send(f'You have sent <:minecoin:955431748081164308>{amount} to {user}')
        except Exception:
            await ctx.send('An error occured')

    # A economy bot fun command
    @commands.command()
    async def gamble(self, ctx, amount: int):
        """ Gamble money"""
        try:
            user_bal = await ecomoney.find_one({"id": ctx.author.id})
            if user_bal is None:
                await self.open_account(ctx.author.id)
                user_bal = await ecomoney.find_one({"id": ctx.author.id})
            if amount > user_bal["wallet"]:
                await ctx.send('You do not have enough money to gamble that much')
            elif amount <= 0:
                await ctx.send('You cannot gamble 0 or less')
            else:
                num = random.randint(1, 100)
                if num <= 50:
                    await ecomoney.update_one({"id": ctx.author.id}, {"$inc": {"wallet": +amount}})
                    await ctx.send(f'You have won <:minecoin:955431748081164308>{amount}')
                elif num > 50:
                    await ecomoney.update_one({"id": ctx.author.id}, {"$inc": {"wallet": -amount}})
                    await ctx.send(f'You have lost <:minecoin:955431748081164308>{amount}')
        except Exception:
            await ctx.send('An error occured')

def setup(bot):
    bot.add_cog(Economy(bot))
