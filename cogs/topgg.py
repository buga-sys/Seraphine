import discord
from discord import client
from discord.ext import commands
import requests
from discord.ext import tasks
import os
from dotenv import load_dotenv
import dbl

load_dotenv()
topgg_token = str(os.getenv('TOPGG_TOKEN'))

class TopGG(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.dblpy = dbl.DBLClient(client, topgg_token, webhook_path='/dblwebhook', webhook_auth='hehexd', webhook_port=8015)
    
    @commands.Cog.listener()
    async def on_dbl_test(data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print(f"Received a test upvote:\n{data}")
        
    @commands.Cog.listener()
    async def on_dbl_vote(data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print(f"Received a test upvote:\n{data}")
        
    @commands.command()
    async def vote(self, ctx):
        user_id = ctx.author.id
        headers = {
                    "Authorization": topgg_token
                    }
        r = requests.get(f'https://top.gg/api//bots/818488537456181248/check?userId={user_id}', headers=headers) 
        voted = r.json()
        vote_link = 'https://top.gg/bot/818488537456181248/vote'
        
        if voted['voted'] == 1:
            embed = discord.Embed(title='Seraphine: Vote' ,description='**Vote to get points and unlock borders to show off in your profile.** \n \u200B \n You already voted. Try again in 12 hours.',color=0xfda5b0)
        else:
            embed = discord.Embed(title='Seraphine: Vote' ,description=f'**Vote to get points and unlock borders to show off in your profile.** \n \u200B \n You can vote every 12 hours. \n [Click here to vote!]({vote_link})',color=0xfda5b0)
        await ctx.send(embed=embed)
        
def setup(client):
    client.add_cog(TopGG(client))