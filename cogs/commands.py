import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client            
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('Missing argument, type `.help` for more information')
        
    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(description='''
                            **ARB IS STILL UNDER DEVELOPMENT**
                            ''', color=0x850000)
        embed.set_thumbnail(url='https://i.imgur.com/7ytdI2o.png')
        embed.set_author(name='ARB', icon_url='https://i.imgur.com/7ytdI2o.png')
        embed.add_field(name="List of commands", value="`?commands`")
        await ctx.send(embed=embed)
    
    @commands.command(name='commands', aliases=['cmds'])
    async def _commands(self, ctx):
        embed=discord.Embed(color=0x850000)
        embed.set_author(name='ARB', icon_url='https://i.imgur.com/7ytdI2o.png')
        embed.add_field(name=":partying_face: Fun", value="`fun`")
        embed.add_field(name=":tools: Utility", value="`utility`")
        embed.add_field(name=":gear: Settings", value="`settings`")
        embed.set_footer(text="use prefix ? before each command.")
        await ctx.send(embed=embed)  

def setup(client):
    client.add_cog(Commands(client))
