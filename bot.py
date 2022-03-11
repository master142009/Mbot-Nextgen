import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands ,tasks
from itertools import cycle

client = commands.Bot(command_prefix="m!")

load_dotenv()

status = cycle(["I am a Modern bot", "Do m!help for all my commands", "I have NextGeneration features"])

@tasks.loop(seconds=5)
async def change_status():  
    await client.change_presence(activity=nextcord.Game(next(status)))

@client.event
async def on_ready():
    change_status.start()
    print(f"{client.user.name} has connected to Discord.")

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        Embed = nextcord.Embed(title="The NextGen Bot", description="Hey! if your new, my prefix is `m!`\nuse `m!help` for all my commands. \n[Invite me](https://discord.com/api/oauth2/authorize?client_id=888675856497643561&permissions=8&scope=bot)", colour=3066993)
        Embed.set_author(name=f"{client.user.name}",
                    icon_url=f"{client.user.avatar.url}")
        Embed.set_footer(
            text=f"Mentioned by {message.author.name}", icon_url=f"{message.author.avatar.url}") 
        await message.channel.send(embed=Embed)

    await client.process_commands(message)

    # load all cogs
for folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", folder, "cog.py")):
        client.load_extension(f"modules.{folder}.cog")

client.run(os.getenv("DISCORD_TOKEN"))
