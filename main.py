import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
token = str(os.getenv('TOKEN'))

client = commands.Bot(command_prefix='!', help_command=None)

@client.event
async def on_ready():
    print("Seraphine has entered the Summoner's Rift.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='!help'))

client.load_extension('cogs.league')
client.load_extension('cogs.champions')
client.load_extension('cogs.items')
client.load_extension('cogs.abilities')
client.load_extension('cogs.commands')
client.load_extension('cogs.ownercommands')
client.load_extension('cogs.other')

client.run(token)
