import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client            
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error
        
    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(description='''
                            **SERAPHINE IS STILL UNDER DEVELOPMENT**
                            ''', color=0xfda5b0)
        embed.set_thumbnail(url='')
        embed.set_author(name='Seraphine', icon_url='')
        embed.add_field(name="List of commands", value="`!commands`")
        await ctx.send(embed=embed)
    
    @commands.command(name='commands', aliases=['cmds'])
    async def _commands(self, ctx):
        embed=discord.Embed(title="Commands", description='''
                            `profile` `history` `champion` `ability` `item` `itemtype`''', color=0xfda5b0)
        embed.set_thumbnail(url='')
        embed.set_footer(text="use prefix ! before each command.")
        await ctx.send(embed=embed)  

def setup(client):
    client.add_cog(Commands(client))
