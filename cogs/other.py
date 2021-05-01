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
        seconds = (now-then).total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        weeks = days / 7
        months = weeks * 0.229984
        date = None
        if seconds < 120:
            date = str(int(minutes)) + ' minute ago'
        elif seconds < 3600:
            date = str(int(minutes)) + ' minutes ago'
        elif seconds < 7200:
            date = str(int(hours)) + ' hour ago'
        elif seconds < 86400:
            date = str(int(hours)) + ' hours ago'
        elif seconds < 172800:
            date = str(int(days)) + ' day ago'
        elif seconds < 604800:
            date = str(int(days)) + ' days ago'
        elif seconds < 1210000:
            date = str(int(weeks)) + ' week ago'
        elif seconds < 2628000:
            date = str(int(weeks)) + ' weeks ago'
        elif seconds < 5256000:
            date = str(int(months)) + ' month ago'
        else:
            date = str(int(months)) + ' months ago'
        
        embed=discord.Embed(title=title, description=f"{author} — {date}", color=0xfda5b0, url=link)
        embed.set_image(url=img_src)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['updates'])
    async def update(self, ctx):
        embed = discord.Embed(description='''
                              Here are the list of changes:
                              \u200B

                              **Added:**
                              (5/1) **!mastery** - You can now view champions with most mastery points of a summoner.
                              
                              \u200B
                              **Improvements:**
                              (5/1) **!counter** - Fixed some champions data couldn't be loaded bug and added more information.
                              ''', color=0xfda5b0)
        embed.set_author(name='Seraphine', icon_url='https://i.pinimg.com/originals/05/e0/8b/05e08be9fd54e6da2f6d482625168c91.png')
        await ctx.send(embed=embed)
            
def setup(client):
    client.add_cog(Other(client))
