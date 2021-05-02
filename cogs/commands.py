import discord
from discord.ext import commands
import asyncio

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client            
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            return
        elif isinstance(error, commands.errors.CommandInvokeError):
            return
        else:
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
        embed.add_field(name=f"{halp} Help", value=f"To contact the developer, submit bugs, or suggest a feature: **BUGA#0001**", inline=False)
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
        buttons = ["1️⃣", "2️⃣", "3️⃣"]
        current = 0
        bow = '<:pink_bow:835176521773350912>'
        
        page1 = discord.Embed(title=f"{bow} Seraphine Commands", 
                              color=0xfda5b0).add_field(
                                name='!ability', 
                                value="Detailed information of a skill.",
                                inline=False).add_field(
                                    name='!add', 
                                    value="Add your summoner to your account.", 
                                    inline=False).add_field(
                                        name='!champion', 
                                        value="Infomation about a champion.", 
                                        inline=False).add_field(
                                            name='!counters', 
                                            value="Champion counters.", 
                                            inline=False).add_field(
                                                name='!history', 
                                                value="Display a summoner's match history.", 
                                                inline=False).add_field(
                                                    name='!invite', 
                                                    value="Invite the bot to your server.", 
                                                    inline=False)
        page2 = discord.Embed(title=f"{bow} Seraphine Commands", 
                              color=0xfda5b0).add_field(
                                name='!item', 
                                value="Detailed information of an item.", 
                                inline=False).add_field(
                                    name='!itemtype',
                                    value="List of items based on type.", 
                                    inline=False).add_field(
                                        name='!mastery', 
                                        value="List of champions with the most mastery points.", 
                                        inline=False).add_field(
                                            name='!matchup', 
                                            value="Champion matchups overview.", 
                                            inline=False).add_field(
                                                name='!patchnotes', 
                                                value="Latest patch notes.", 
                                                inline=False).add_field(
                                                    name='!profile', 
                                                    value="Display a summoner's profile.", 
                                                    inline=False)
        page3 = discord.Embed(title=f"{bow} Seraphine Commands", 
                              color=0xfda5b0).add_field(
                                name='!rankings', 
                                value="List of top players.", 
                                inline=False).add_field(
                                    name='!remove', 
                                    value="Remove added summoner from your account.", 
                                    inline=False).add_field(
                                        name='!rotation', 
                                        value="Weekly free-to-play champion rotation.", 
                                        inline=False).add_field(
                                            name='!skins', 
                                            value="List of a champion's skins.", 
                                            inline=False).add_field(
                                                name='!update', 
                                                value="Check Seraphine latest updates.", 
                                                inline=False)
        
        pages = [page1, page2, page3]

        msg = await ctx.send(embed=pages[current].set_footer(text=f"Page {current+1}ᅠ•ᅠNavigate through pages using the reactions below!"))

        for button in buttons:
            await msg.add_reaction(button)
            
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons and reaction.message.id == msg.id, timeout=30.0)

            except asyncio.TimeoutError:
                pass

            else:
                previous_page = current
                if reaction.emoji == "1️⃣":
                    current = 0
                    await msg.remove_reaction("1️⃣", ctx.author)
                    
                elif reaction.emoji == "2️⃣":
                    current = 1
                    await msg.remove_reaction("2️⃣", ctx.author)
                        
                elif reaction.emoji == "3️⃣":
                    current = 2
                    await msg.remove_reaction("3️⃣", ctx.author)

                if current != previous_page:
                    await msg.edit(embed=pages[current].set_footer(text=f"Page {current+1}ᅠ•ᅠNavigate through pages using the reactions below!"))  

def setup(client):
    client.add_cog(Commands(client))
