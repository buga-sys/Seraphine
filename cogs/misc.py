import discord
from discord.ext import commands
import requests
import bs4
from datetime import datetime
import os

ops = '<:outage:835522354963677184>'

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client              
        
    @commands.command(aliases=['patchnote'])
    async def patchnotes(self, ctx):
        def td_format(td_object):
            seconds = int(td_object.total_seconds())
            periods = [
                ('year',        60*60*24*365),
                ('month',       60*60*24*30),
                ('day',         60*60*24),
                ('hour',        60*60),
                ('minute',      60),
                ('second',      1)
            ]

            strings=[]
            for period_name, period_seconds in periods:
                if seconds > period_seconds:
                    period_value , seconds = divmod(seconds, period_seconds)
                    has_s = 's' if period_value > 1 else ''
                    strings.append("%s %s%s" % (period_value, period_name, has_s))

            return ", ".join(strings)
        
        page = requests.get('https://na.leagueoflegends.com/en-us/news/tags/patch-notes')
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        latest_article = soup.find_all('li')[0]
        img_src = latest_article.find('img')['src']
        href = latest_article.find('a')['href']
        title = latest_article.find('h2').text
        link = 'http://na.leagueoflegends.com' + href
        author = latest_article.find(class_='style__Author-i44rc3-11 gaoSwO').text
        ar_time = latest_article.find('time')['datetime']
        then = datetime.strptime(ar_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.now()
        seconds = (now-then)
        date = td_format(seconds)
        
        embed=discord.Embed(title=title, description=f"{author} — {date}", color=0xfda5b0, url=link)
        embed.set_image(url=img_src)
        await ctx.send(embed=embed)
            
def setup(client):
    client.add_cog(Misc(client))
