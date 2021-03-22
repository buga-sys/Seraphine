import discord
from discord.ext import commands
import json

api = 'RGAPI-6a15b991-08e8-4373-bcde-83594bdc51a6'
version = '11.6.1'

class Champions(commands.Cog):
    def __init__(self, client):
        self.client = client   
   
    @commands.command(aliases=['i'])
    async def item(self, ctx, value):
        with open(f'dragontail\\{version}\\data\\en_GB\\item.json', encoding='utf-8') as f:
            item = json.load(f)
        f.close()

def setup(client):
    client.add_cog(Champions(client))