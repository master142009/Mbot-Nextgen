import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands ,tasks, activities
from itertools import cycle
from nextcord.ui import Button, View

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
    hi = Button(label="Invite me", url="https://discord.com/api/oauth2/authorize?client_id=888675856497643561&permissions=8&scope=bot")
    myview = View(timeout=180)
    myview.add_item(hi)
    if client.user.mentioned_in(message):
        Embed = nextcord.Embed(title="The NextGen Bot's Sweet help!", description="Hey! if your new, my prefix is `m!`\nuse `m!help` for all my commands.", colour=3066993)
        Embed.set_author(name=f"{client.user.name}",
                    icon_url=f"{client.user.avatar.url}")
        Embed.set_footer(
            text=f"Mentioned by {message.author.name}", icon_url=f"{message.author.avatar.url}", text = time)
        Embed.set_thumbnail(url="https://m.economictimes.com/thumb/msid-69278189,width-1200,height-900,resizemode-4,imgsize-74151/help-getty.jpg")     
        await message.channel.send(embed=Embed, view=myview)

    await client.process_commands(message)


    # load all cogs
for folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", folder, "cog.py")):
        client.load_extension(f"modules.{folder}.cog")

client.run(os.getenv("DISCORD_TOKEN"))
