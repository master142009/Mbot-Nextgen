import nextcord
from nextcord.ext import commands
import random
from random import choice
import aiosqlite
from easy_pil import *
import datetime, time

class Random(commands.Cog, name="Random"):
    """Returns random results"""

    COG_EMOJI = "🎲"

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, Sorry, you do not have permission to do this! `Required Permission: Administrator`")
        print(type(ctx), type(error))        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Level Cog ready!")
        setattr(self.bot, "db", await aiosqlite.connect("level.db"))
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        author = message.author
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id,))

            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

            if level < 5:
                xp += random.randint(1, 3)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
            else:
                rand = random.randint(1, (level//4))
                if rand == 1:
                    xp += random.randint(1, 3)
                    await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
            if xp >= 100:
                level += 1
                await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id,))
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
                await message.channel.send(f"{author.mention} you have reached to level **{level}**!")
        await self.bot.db.commit()            

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

    @commands.command(aliases=['lvl', 'level', 'r'])
    async def rank(self, ctx, member: nextcord.Member = None):
        """Shows people's rank."""
        if member is None:
            member = ctx.author    
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id,))
                await self.bot.db.commit()

            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

            if xp < 5:
                percentage = 4
            else:
                percentage = xp   

            user_data = {
                "name": f"{member.name}",
                "xp": xp,
                "level": level,
                "next_level_up": 100,
                "percentage": percentage,
            }

            background = Editor("modules/random/background.png")           
            profile_picture = await load_image_async(str(member.avatar.url))
            profile = Editor(profile_picture).resize((150, 150)).circle_image()

            poppins = Font.poppins(size=40)
            poppins_small  = Font.poppins(size=30)

            card_image_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

            background.polygon(card_image_shape, color="#90EE90")
            background.paste(profile, (30, 30))

            background.rectangle((30, 220), width=650, height=40, color="#90EE90", radius=20)
            background.bar((30, 220), max_width=650, height=40, percentage=user_data["percentage"], color="#66ff00", radius=20,)
            background.text((200, 40), user_data["name"], font=poppins, color="#FFFF00")

            background.rectangle((200, 100), width=350, height=2, fill="#90EE90")
            background.text(
                (200, 130),
                f"Level - {user_data['level']}  |  {user_data['xp']} / {user_data['next_level_up']}",
                font = poppins_small,
                color = "#FFFF00",
            )

            file = nextcord.File(fp=background.image_bytes, filename="levelcard.png")
            await ctx.send(file=file)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, member: nextcord.Member):
        """Resets people's rank."""
        if member is None:
            member = ctx.author    
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id,))
                await self.bot.db.commit()

            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0
            
            level = 0
            await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, member.id, ctx.guild.id,))
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, member.id, ctx.guild.id,))
            await ctx.send(f"{member.mention} has been reset!")

    @commands.command(name='8ball')
    async def _8ball(self, ctx):
        """!8ball - Ask the Magic 8-Ball."""
        icon_url = 'https://i.imgur.com/XhNqADi.png'
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Do not count on it.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
            ]
        fortune = random.choice(responses)

        embed = nextcord.Embed(colour=nextcord.Colour.purple())
        embed.set_author(name='Magic 8-Ball', icon_url=icon_url)
        embed.add_field(name=f'*{ctx.author.name}, your fortune says...*', value=f'**{fortune}**')
        await ctx.send(embed=embed)            
            
                               

    
    

def setup(bot: commands.Bot):
    bot.add_cog(Random(bot))
