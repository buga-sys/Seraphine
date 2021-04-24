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
    
    @commands.command()
    async def status(self, ctx, region=None):
        regions = ['euw', 'br', 'na', 'eune', 'jp', 'las', 'lan', 'oc', 'tr', 'kr', 'ru']
        servers = {'euw':'euw1','br':'br1', 'na':'na1', 'eune':'eun1', 'jp':'jp1', 'las':'la2', 'lan':'la1', 'oc':'oc1', 'tr':'tr1', 'kr':'kr', 'ru':'ru'}
        online = '<:status_online_large:835174687528714311>'
        offline = '<:status_offline_large:835174688065323068>'
        
        if region is None:
            all_regions = ['br1','eun1','euw1','jp1','kr','la1','la2','na1','oc1','ru','tr1']
            embed=discord.Embed(title='League of Legends Status', description='All servers:', color=0xfda5b0)
            embed.set_thumbnail(url='https://seraphine-bot.s3.eu-central-1.amazonaws.com/lol_icon_32.png')
            for r in all_regions:
                lol = requests.get(f'https://{r}.api.riotgames.com/lol/status/v3/shard-data?api_key={api}')
                name = lol.json()['slug']
                status = lol.json()['services'][0]['status']
                e_status = online if status == 'online' else offline
                embed.add_field(name=f'{name.upper()}', value=f"{e_status}")
            embed.add_field(name='\u200B', value=f"\u200B")
            embed.add_field(name='\u200B', value=f"for in-depth status, `!status [region]`", inline=False)
            await ctx.send(embed=embed)
        elif region.lower() in regions:
            for k,v in servers.items():
                if region.lower() == k:
                    server = v
            lol = requests.get(f'https://{server}.api.riotgames.com/lol/status/v3/shard-data?api_key={api}') 
            server_name = lol.json()['name']
            server_slug = lol.json()['slug']
            services = lol.json()['services']
                 
            embed=discord.Embed(title=f'League of Legends Status: {server_slug.upper()}', description=f'{server_name} server report:', color=0xfda5b0)
            embed.set_thumbnail(url='https://seraphine-bot.s3.eu-central-1.amazonaws.com/lol_icon_32.png')
            for s in services:
                name = s['name']
                status = s['status']
                e_status = online if status == 'online' else offline
                embed.add_field(name=f'{name}', value=f"{e_status}")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f'{ops} Seraphine: Status', description="Invalid region!", color=0xfda5b0)
            embed.add_field(name='Regions', value='`br` `eune` `euw` `jp` `kr` `lan` `las` `na` `oce` `ru` `tr`')
            await ctx.send(embed=embed)
            
            
            
            
        
        

def setup(client):
    client.add_cog(Other(client))
