import os
from nextcord import ButtonStyle, Status
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands ,tasks
from itertools import cycle
from nextcord.ui import Button, View
import datetime
import lavalink

client = commands.Bot(command_prefix="m?")

client.lavalink_nodes = [
    {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"},
    # Can have multiple nodes here
]

load_dotenv()

changestatus = cycle(["I am a Modern bot", "Do m?help for all my commands", "I have NextGeneration features"])

@tasks.loop(seconds=5)
async def change_status_text():  
    await client.change_presence(activity=nextcord.Game(next(changestatus)))  

@client.event
async def on_ready():
    change_status_text.start()
    client.load_extension('dismusic')
    print(f"{client.user.name} has connected to Discord.")        

@client.event
async def on_message(message):
    hi = Button(label="Invite me", url="https://discord.com/api/oauth2/authorize?client_id=888675856497643561&permissions=8&scope=bot")
    yt = Button(label="Youtube", style=ButtonStyle.url, url="https://www.youtube.com/channel/UCl2Bbv8trRunL9YAGsbGOqQ" )
    myview = View(timeout=180)
    myview.add_item(hi)
    myview.add_item(yt)
    if client.user.mentioned_in(message):
        Embed = nextcord.Embed(title="The NextGen Bot's Sweet help!", description="Hey! thx for mentioning me\nif your new, my prefix is `m?`\nuse `m?help` for all my commands.", colour=3066993)
        Embed.set_author(name=f"{client.user.name}",
                    icon_url=f"{client.user.avatar.url}")
        Embed.set_footer(
            text=f"Mentioned by {message.author.name}", icon_url=f"{message.author.avatar.url}")
        Embed.set_thumbnail(url="https://m.economictimes.com/thumb/msid-69278189,width-1200,height-900,resizemode-4,imgsize-74151/help-getty.jpg")
        Embed.timestamp = datetime.datetime.utcnow()     
        await message.channel.send(embed=Embed, view=myview)

    await client.process_commands(message)


    # load all cogs
for folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", folder, "cog.py")):
        client.load_extension(f"modules.{folder}.cog")

client.run(os.getenv("DISCORD_TOKEN"))
