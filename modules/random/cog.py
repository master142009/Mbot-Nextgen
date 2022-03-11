import nextcord
from nextcord.ext import commands
import random
from random import choice

class Random(commands.Cog, name="Random"):
    """Returns random results"""

    COG_EMOJI = "🎲"

    def __init__(self, bot: commands.Bot):
        self._bot = bot    

    @commands.command()
    async def roll(self, ctx: commands.Context, dice: str):
        """Rolls a given amount of dice in the form \_d\_
        
        Example:
        ```
        m!roll 2d20
        ```
        """
        try:
            rolls = ""
            total = 0
            amount, die = dice.split("d")
            for _ in range(int(amount)):
                roll = random.randint(1, int(die))
                total += roll
                rolls += f"{roll} "
            await ctx.send(f"Rolls: {rolls}\nSum: {total}")
        except ValueError:
            await ctx.send("Dice must be in the format \_d\_ (example: 2d6)")

    @commands.command()
    async def choose(self, ctx: commands.Context, *args):
        """Chooses a random item from a list
        
        Example:
        ```
        ?choose "First Option" "Second Option" "Third Option"
        ```
        """
        try:
            choice = random.choice(args)
            await ctx.send(choice)
        except IndexError:
            await ctx.send("You must specify at least one argument.")

    @commands.command()
    async def toss(self, ctx):
        """heads or tail"""
        toss = ['Oh its a head', 'Oh its a tail']
        await ctx.send(f"{random.choice(toss)}")

    @commands.command()
    async def emojify(self, ctx,*,text):
        """Converts text to emojify"""
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2word = {
                    '0':'zero','1':'one','2':'two',
                    '3':'three','4':'four','5':'five',
                    '6':'six','7':'seven','8':'eight','9':'nine'}
                emojis.append(f':{num2word.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)
        await ctx.send(''.join(emojis))

    
    

def setup(bot: commands.Bot):
    bot.add_cog(Random(bot))
