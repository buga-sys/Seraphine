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
        embed=discord.Embed(description='''
                            **SERAPHINE IS STILL UNDER DEVELOPMENT**
                            ''', color=0xfda5b0)
        embed.set_thumbnail(url='')
        embed.set_author(name='Seraphine', icon_url='')
        embed.add_field(name="List of commands", value="`!commands`")
        await ctx.send(embed=embed)
    
    @commands.command(name='commands', aliases=['cmds'])
    async def _commands(self, ctx):
        url = 'http://google.com/'
        profile = f"""[`profile`]({url} "Display a summoner's profile.")"""
        myprofile = f"""[`myprofile`]({url} "Display your summoner's profile.")"""
        history = f"""[`history`]({url} "Display a summoner's match history.")"""
        champion = f"""[`champion`]({url} "See information about a champion.")"""
        skins = f"""[`skins`]({url} "View all champion's skins.")"""
        ability = f"""[`ability`]({url} "View a specific champion's skill.")"""
        item = f"""[`item`]({url} "See detailed information of an item.")"""
        itemtype = f"""[`itemtype`]({url} "Look up item types: ability, attack speed, armor, etc.")"""
        
        embed=discord.Embed(title="Commands", description=f'''
                            {profile} {myprofile} {history} {champion} {skins} {ability} {item} {itemtype}''', color=0xfda5b0)
        embed.set_thumbnail(url='')
        embed.set_footer(text="use prefix ! before each command.")
        await ctx.send(embed=embed)  

def setup(client):
    client.add_cog(Commands(client))
