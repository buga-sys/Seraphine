import discord
from discord.ext import commands
import os

class OwnerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client 
    
    @commands.command(name='servers', hidden=True)
    @commands.is_owner()
    async def _servers(self, ctx):
        guildcount = len(self.client.guilds)
        activeservers = self.client.guilds
        print('********************** GUILD LIST **********************')
        for guild in activeservers:
            print(f'{guild.name} - ({guild.id})')
        print(f'Seraphine is in {guildcount} servers.')   
    
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
            await ctx.author.send('hehe xd cogs reloaded.') 
    
    @commands.command(name='leave', hidden=True)
    @commands.is_owner()
    async def _leaveserver(self, ctx, *, guild_id):
        guild = self.client.get_guild(int(guild_id))
        if guild is None:
            await ctx.send("I don't recognize that guild.")
            return
        await guild.leave()
        await ctx.send(f"Left guild: {guild.name} ({guild.id})")
    
    
        
def setup(client):
    client.add_cog(OwnerCommands(client))