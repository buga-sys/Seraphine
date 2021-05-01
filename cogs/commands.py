import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client            
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            return
        raise error   
        
    @commands.command()
    async def help(self, ctx):
        inv = '<:invite:835844574404018177>'
        cmd = '<:cmd:835632392307867739>'
        halp = '<:help:835845004915245096>'
        invite_link = 'https://discord.com/oauth2/authorize?client_id=818488537456181248&permissions=321600&scope=bot'
        contact_link = 'https://discordapp.com/channels/@me/161750634251419648/'
        embed=discord.Embed(color=0xfda5b0)
        embed.set_author(name=f'Seraphine Help')
        embed.add_field(name=f"{cmd} Commands", value="To see list of commands: `!commands`", inline=False)
        embed.add_field(name=f"{inv} Invite", value=f"Click [**here**]({invite_link}) to invite the bot to your server.", inline=False)
        # embed.add_field(name=f"{halp} Help", value=f"To contact the developer, submit bugs, or suggest a feature, click [**here**]({contact_link}).", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def invite(self, ctx):
        inv = '<:invite2:835841084147630110>'
        invite_link = 'https://discord.com/oauth2/authorize?client_id=818488537456181248&permissions=321600&scope=bot'
        embed=discord.Embed(title=f'{inv} Seraphine Invite', description="Here's the link to invite the bot to your server!", color=0xfda5b0)
        embed.add_field(name="Invite", value=f"[**Click here**]({invite_link})", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='commands', aliases=['cmds'])
    async def _commands(self, ctx):
        bow = '<:pink_bow:835176521773350912>'
        embed=discord.Embed(title=f"{bow} Seraphine Commands", color=0xfda5b0)
        embed.add_field(name='ability', value="Detailed information of a skill.", inline=False)
        embed.add_field(name='add', value="Add your summoner to your account.", inline=False)
        embed.add_field(name='champion', value="Infomation about a champion.", inline=False)
        embed.add_field(name='counters', value="Champion counters.", inline=False)
        embed.add_field(name='history', value="Display a summoner's match history.", inline=False)
        embed.add_field(name='invite', value="Invite the bot to your server.", inline=False)
        embed.add_field(name='item', value="Detailed information of an item.", inline=False)
        embed.add_field(name='itemtype', value="List of items based on type.", inline=False)
        embed.add_field(name='mastery', value="List of champions with the most mastery points.", inline=False)
        embed.add_field(name='matchup', value="Champion matchups overview.", inline=False)
        embed.add_field(name='patchnotes', value="Latest patch notes.", inline=False)
        embed.add_field(name='profile', value="Display a summoner's profile.", inline=False)
        embed.add_field(name='remove', value="Remove added summoner from your account.", inline=False)
        embed.add_field(name='rotation', value="Weekly free-to-play champion rotation.", inline=False)
        embed.add_field(name='skins', value="List of a champion's skins.", inline=False)
        embed.add_field(name='update', value="Check Seraphine latest updates.", inline=False)
        embed.set_footer(text="use prefix ! before each command.")
        await ctx.send(embed=embed)  

def setup(client):
    client.add_cog(Commands(client))
