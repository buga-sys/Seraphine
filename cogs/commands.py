import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client            
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
    @commands.command()
    async def help(self, ctx):
        invite_link = 'https://discord.com/oauth2/authorize?client_id=818488537456181248&permissions=59392&scope=bot'
        embed=discord.Embed(color=0xfda5b0)
        embed.set_thumbnail(url='')
        embed.set_author(name='Seraphine', icon_url='')
        embed.add_field(name="Commands", value="To see list of commands: `!commands`", inline=False)
        embed.add_field(name="Invite", value=f"Click [here]({invite_link}) to invite the bot to your server.", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='commands', aliases=['cmds'])
    async def _commands(self, ctx):
  
        embed=discord.Embed(title="Commands", color=0xfda5b0)
        embed.add_field(name='profile', value="Display a summoner's profile.", inline=False)
        embed.add_field(name='myprofile', value="Display your summoner's profile.", inline=False)
        embed.add_field(name='history', value="Display a summoner's match history.", inline=False)
        embed.add_field(name='champion', value="Infomation about a champion.", inline=False)
        embed.add_field(name='ability', value="Detailed information of a skill.", inline=False)
        embed.add_field(name='skins', value="List of a champion's skins.", inline=False)
        embed.add_field(name='item', value="Detailed information of an item.", inline=False)
        embed.add_field(name='itemtype', value="List of items based on type.", inline=False)
        embed.add_field(name='patchnotes', value="Latest patch notes.", inline=False)
        embed.set_thumbnail(url='')
        embed.set_footer(text="use prefix ! before each command.")
        await ctx.send(embed=embed)  

def setup(client):
    client.add_cog(Commands(client))
