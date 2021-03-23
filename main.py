import discord
from discord.ext import commands

client = commands.Bot(command_prefix='?', help_command=None)

@client.event
async def on_ready():
    print("Seraphine has entered the Summoner's Rift.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='League of Legends'))

client.load_extension('cogs.league')
client.load_extension('cogs.champions')
client.load_extension('cogs.items')
client.load_extension('cogs.abilities')
client.load_extension('cogs.commands')

client.run('ODE4NDg4NTM3NDU2MTgxMjQ4.YEYy2g.7Pa84mtVXUw8rER23v6zxlwyq4g')
