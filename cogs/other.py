import discord
from discord.ext import commands
import requests
import bs4
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
api = str(os.getenv('API_KEY'))

ops = '<:outage:835522354963677184>'

class Other(commands.Cog):
    def __init__(self, client):
        self.client = client              
        
    @commands.command(aliases=['patchnote'])
    async def patchnotes(self, ctx):
        page = requests.get('https://na.leagueoflegends.com/en-us/news/tags/patch-notes')
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        latest_article = soup.find_all('li')[0]
        img_src = latest_article.find('img')['src']
        href = latest_article.find('a')['href']
        title = latest_article.find('h2').text
        link = 'http://na.leagueoflegends.com' + href
        author = latest_article.find(class_='style__Author-i44rc3-11 gaoSwO').text
        time = latest_article.find('time')['datetime']
        then = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.now()
        days = str((now-then).days) + ' days ago'
        
        embed=discord.Embed(title=title, description=f"{author} — {days}", color=0xfda5b0, url=link)
        embed.set_image(url=img_src)
        await ctx.send(embed=embed)
            
def setup(client):
    client.add_cog(Other(client))
