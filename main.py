import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import tasks
import asyncio
import os

load_dotenv()
token = str(os.getenv('TOKEN'))

client = commands.Bot(command_prefix='!', help_command=None)

@tasks.loop(seconds=120.0)
async def my_background_task():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='!help'))
    await asyncio.sleep(60)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='on patch: 11.9'))

@client.event
async def on_ready():
    print("Seraphine has entered the Summoner's Rift.")
    await client.wait_until_ready()
    my_background_task.start()

client.load_extension('cogs.summoner')
client.load_extension('cogs.accounts')
client.load_extension('cogs.champions')
client.load_extension('cogs.items')
client.load_extension('cogs.abilities')
client.load_extension('cogs.commands')
client.load_extension('cogs.ownercommands')
client.load_extension('cogs.misc')
client.load_extension('cogs.topgg')

client.run(token)
