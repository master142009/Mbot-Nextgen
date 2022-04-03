import os
from nextcord import ButtonStyle, Status
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands ,tasks
from itertools import cycle
from nextcord.ui import Button, View
import datetime
import lavalink
import json    
import aiosqlite
import random
import asyncio
import jishaku

def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(message.guild.id), "m?")    

client = commands.Bot(command_prefix=get_prefix, intents = nextcord.Intents.all())

client.lavalink_nodes = [
    {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"},
    # Can have multiple nodes here
]

load_dotenv()

changestatus = cycle(["I am a Modern bot in making",
 f"Ping me for some help!",
  "I have NextGeneration features",
  "Mbot V3",
  "Minecraft 1.19",
  "ROCKING RUMMY | Youtuber"])

@tasks.loop(seconds=5)
async def change_status_text():  
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Game(next(changestatus)))            

@client.event
async def on_ready():
    client.uptime = datetime.datetime.utcnow()
    change_status_text.start()
    print(f"{client.user.name} has connected to Discord.")                             

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'm?'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)            

@client.event
async def on_message(message):
    hi = Button(label="Invite me", url="https://discord.com/api/oauth2/authorize?client_id=888675856497643561&permissions=8&scope=bot")
    yt = Button(label="Youtube", style=ButtonStyle.url, url="https://www.youtube.com/channel/UCl2Bbv8trRunL9YAGsbGOqQ" )
    myview = View(timeout=180)
    myview.add_item(hi)
    myview.add_item(yt)
    if client.user.mentioned_in(message):
        Embed = nextcord.Embed(title="The NextGen Bot's Sweet help!", description=f"Hey! thx for mentioning me\nif your new, my prefix is `m?`\nuse `m?help` for all my commands.", colour=3066993)
        Embed.set_author(name=f"{client.user.name}",
                    icon_url=f"{client.user.avatar.url}")
        Embed.set_footer(
            text=f"Mentioned by {message.author.name}", icon_url=f"{message.author.avatar.url}")
        Embed.set_thumbnail(url="https://m.economictimes.com/thumb/msid-69278189,width-1200,height-900,resizemode-4,imgsize-74151/help-getty.jpg")
        Embed.timestamp = datetime.datetime.utcnow()     
        await message.channel.send(embed=Embed, view=myview)    

    await client.process_commands(message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('m?AI'):
        e = nextcord.Embed(title="Mbot AI", description="AI version of me [Invite AI me](https://discord.com/oauth2/authorize?client_id=959359412236070923&scope=bot&permissions=8)")
        await message.channel.send(embed=e)

    await client.process_commands(message)               


    # load all cogs
for folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", folder, "cog.py")):
        client.load_extension(f"modules.{folder}.cog")

client.load_extension("jishaku")
client.run(os.getenv("DISCORD_TOKEN"))
