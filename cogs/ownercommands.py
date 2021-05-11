import discord
from discord.ext import commands
import os
import json

class OwnerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client 
    
    @commands.command(name='servers', hidden=True)
    @commands.is_owner()
    async def _servers(self, ctx):
        guildcount = len(self.client.guilds)
        activeservers = self.client.guilds
        print(f'Seraphine is in {guildcount} guilds.')   
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module : str):
        cog = f'cogs.{module}'
        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.author.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.author.send(f'{cog} loaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module : str):
        cog = f'cogs.{module}'
        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.author.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.author.send(f'{cog} unloaded.')  

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module : str):
        cog = f'cogs.{module}'
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.author.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.author.send(f'{cog} reloaded.')  
            
    @commands.command(name='reloadall', hidden=True)
    @commands.is_owner()
    async def _reloadall(self, ctx):
        try:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.client.unload_extension(f'cogs.{filename[:-3]}')
                    self.client.load_extension(f'cogs.{filename[:-3]}')
                    await ctx.author.send(f'cogs.{filename[:-3]} reloaded')
        except Exception as e:
            await ctx.author.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.author.send('*** cogs reloaded ***') 
    
    @commands.command(name='leave', hidden=True)
    @commands.is_owner()
    async def _leaveserver(self, ctx, *, guild_id):
        guild = self.client.get_guild(int(guild_id))
        if guild is None:
            await ctx.send("I don't recognize that guild.")
            return
        await guild.leave()
        await ctx.send(f"Left guild: {guild.name} ({guild.id})")
    
    @commands.command()
    @commands.is_owner()
    async def emojis(self, ctx):   
        with open('data/summonerIcons.json', 'r') as filename:
            data = json.load(filename)
            
            with open(f'dragontail/11.9.1/data/en_GB/summoner.json', encoding="utf8") as f:
                champion = json.load(f)       
            for emoji in ctx.guild.emojis:
                for k,v in champion['data'].items():
                    if v['id'] == emoji.name:
                        emojis = {"id": v['id'],
                                "name": v['name'], 
                                "emoji": f"<:{emoji.name}:{emoji.id}>"
                            }
                        data.append(emojis)
            f.close() 
            with open('data/summonerIcons.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)
    
    @commands.command()
    @commands.is_owner()
    async def rules(self, ctx):
        embed = discord.Embed(description='''
                                **1)** Be mature. Use common sense. Be appropriate.

                                **2)** Respect each other’s opinions, conversation, and DMs.

                                **3)** There is no reason to advertise here.

                                **4)** There will be no lewd, inappropriate, and sexual talk or posting.

                                **5)** Any racist, homophobic/transphobic, sexist comments or slangs will not be tolerated.

                                **6)** Follow each topic for channels. Please, read what you’re supposed to be doing in each channel.
                              ''',color=0xfda5b0).set_author(
                                  name='Server Rules', 
                                  icon_url=''
                              ).set_image(url='https://seraphine-bot.s3.eu-central-1.amazonaws.com/rules.png')
        await ctx.send(embed=embed)
                   
def setup(client):
    client.add_cog(OwnerCommands(client))