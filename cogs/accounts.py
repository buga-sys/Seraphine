import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv
import mysql.connector
import traceback
import requests

api = str(os.getenv('API_KEY'))
version = str(os.getenv('VERSION'))

host = str(os.getenv('HOST'))
database = str(os.getenv('DATABASE'))
user = str(os.getenv('USER'))
password = str(os.getenv('PASSWORD'))
port = str(os.getenv('PORT'))

ops = '<:outage:835522354963677184>'
check = '<:check:835842893696204830>'

class Accounts(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def add(self, ctx, region=None, *, summoner=None):
        user_id = ctx.author.id
        regions = ['euw', 'br', 'na', 'eune', 'jp', 'las', 'lan', 'oce', 'tr', 'kr', 'ru']
        if region is None and summoner is None:
            embed=discord.Embed(title=f'{ops} Seraphine: Add', description="Please give me a region and a summoner!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!add [region] [summoner]`')
            await ctx.send(embed=embed)
        elif region.lower() not in regions:
            embed=discord.Embed(title=f'{ops} Seraphine: Add', description="Invalid region!", color=0xfda5b0)
            embed.add_field(name='Regions', value='`br` `eune` `euw` `jp` `kr` `lan` `las` `na` `oce` `ru` `tr`')
            await ctx.send(embed=embed)  
        elif summoner is None:
            embed=discord.Embed(title=f'{ops} Seraphine: Add', description="You're missing something!", color=0xfda5b0)
            embed.add_field(name='To add your profile', value='`!myprofile [region] [summoner]`')
            await ctx.send(embed=embed) 
        else:
            try:
                conn = mysql.connector.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=password,
                    port=port)
                
                cur = conn.cursor()
                cur.execute(f"""SELECT * FROM profile WHERE user_id = '{user_id}'""")
                data = cur.fetchone()
                if data is not None:
                    embed=discord.Embed(title=f'{ops} Seraphine: Add', description="**You already have a summoner added to your account!** \n \u200B \n To change it, you need to remove it by using the `!remove` command first.", color=0xfda5b0)
                    await ctx.send(embed=embed) 
                else:
                    cur.execute(f"""INSERT INTO profile(user_id, region, summoner)
                                VALUES ('{user_id}', '{region}', '{summoner}')""")
                    conn.commit()
                    cur.close()
                    
                    servers = {'euw':'euw1','br':'br1', 'na':'na1', 'eune':'eun1', 'jp':'jp1', 'las':'la2', 'lan':'la1', 'oce':'oc1', 'tr':'tr1', 'kr':'kr', 'ru':'ru'}
                    for k,v in servers.items():
                        if region.lower() == k:
                            server = v
                    try:
                        summoner_request = requests.get(f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api}')
                    except Exception:
                        traceback.print_exc()
                    summoner_json = summoner_request.json()
                    icon_id = summoner_json['profileIconId']
                    
                    with open(f'dragontail/{version}/data/en_GB/profileicon.json') as f:
                        icon = json.load(f)
                    icon_path = f'dragontail/{version}/img/profileicon/'
                    icon_png = icon['data'][f'{icon_id}']['image']['full']
                    icon_full_path = icon_path + icon_png
                    f.close()
                    
                    file = discord.File(f"{icon_full_path}", filename=f"{icon_png}")
                    embed=discord.Embed(title=f'{check} Seraphine: Add', description="This summoner has been added to your account.", color=0xfda5b0)
                    embed.set_author(name=f'{summoner} [{region.upper()}]', icon_url=f'attachment://{icon_png}')
                    await ctx.send(file=file, embed=embed)
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
            else:
                if conn is not None:
                    conn.close()
                    
    @commands.command()
    async def remove(self, ctx):
        user_id = ctx.author.id
        try:
            conn = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port)
            
            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM profile WHERE user_id = '{user_id}'""")
            data = cur.fetchone()
            if data is None:
                embed=discord.Embed(title=f'{ops} Seraphine: Remove', description="You don't have a summoner added to your account.", color=0xfda5b0)
                await ctx.send(embed=embed)
            else:
                profile_data = list(data)
                region = profile_data[1]
                summoner = profile_data[2]
                embed=discord.Embed(title=f'{check} Seraphine: Remove', description=f"**{summoner} [{region.upper()}] has been removed from your account!** \n \u200B \n To link a new summoner, use the `!add` command.", color=0xfda5b0)
                await ctx.send(embed=embed)
                cur.execute(f"""DELETE FROM profile WHERE user_id = '{user_id}'""")
                conn.commit()
                cur.close()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        else:
            if conn is not None:
                conn.close()

def setup(client):
    client.add_cog(Accounts(client))