import discord
from discord.ext import commands
import requests
import json
import traceback
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
api = str(os.getenv('API_KEY'))
version = str(os.getenv('VERSION'))

host = str(os.getenv('HOST'))
database = str(os.getenv('DATABASE'))
user = str(os.getenv('USER'))
password = str(os.getenv('PASSWORD'))
port = str(os.getenv('PORT'))

ops = '<:outage:835522354963677184>'
check = '<:check:835537223138803802>'
                
class League(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def profile(self, ctx, region=None, *, summoner=None):
        regions = ['euw', 'br', 'na', 'eune', 'jp', 'las', 'lan', 'oce', 'tr', 'kr', 'ru']
        servers = {'euw':'euw1','br':'br1', 'na':'na1', 'eune':'eun1', 'jp':'jp1', 'las':'la2', 'lan':'la1', 'oce':'oc1', 'tr':'tr1', 'kr':'kr', 'ru':'ru'}
        if region is None and summoner is None:
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
                if data is not None:
                    profile_data = list(data)
                    region = profile_data[1]
                    summoner = profile_data[2]
                    await self.profile(ctx, region, summoner=summoner)
                else:
                    embed=discord.Embed(title=f'{ops} Seraphine: Profile', description="You dont have a summoner added! \n \u200B \n Add your profile so you don't have to specify your account information.", color=0xfda5b0)
                    embed.add_field(name='Add Your Summoner', value='`!add [region] [summoner]`')
                    embed.add_field(name='Specify', value='`!profile [region] [summoner]`')
                    await ctx.send(embed=embed)
                cur.close()
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
            else:
                if conn is not None:
                    conn.close()
                              
        elif region.lower() not in regions:
            embed=discord.Embed(title=f'{ops} Seraphine: Profile', description="Invalid region!", color=0xfda5b0)
            embed.add_field(name='Regions', value='`br` `eune` `euw` `jp` `kr` `lan` `las` `na` `oce` `ru` `tr`')
            await ctx.send(embed=embed)
        elif summoner is None:
            embed=discord.Embed(title=f'{ops} Seraphine: Profile', description="You're missing something!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!profile [region] [summoner]`')
            await ctx.send(embed=embed)
        else:
            for k,v in servers.items():
                if region.lower() == k:
                    server = v
            try:
                try:
                    summoner_request = requests.get(f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api}')
                except Exception:
                    traceback.print_exc()
                summoner_json = summoner_request.json()
                summoner_id = summoner_json['id']
                account_id = summoner_json['accountId']
                name = summoner_json['name']
                level = summoner_json['summonerLevel']
                icon_id = summoner_json['profileIconId']
                
                with open(f'dragontail/{version}/data/en_GB/profileicon.json') as f:
                    icon = json.load(f)
                icon_path = f'dragontail/{version}/img/profileicon/'
                icon_png = icon['data'][f'{icon_id}']['image']['full']
                icon_full_path = icon_path + icon_png
                f.close()
                
                file = discord.File(f"{icon_full_path}", filename=f"{icon_png}")
                temp_embed = discord.Embed(description=f"Fetching {name}'s profile, wait a moment...", color=0xfda5b0)
                temp_embed.set_thumbnail(url=f'attachment://{icon_png}')
                msg = await ctx.send(embed=temp_embed, file=file)
                
                try:
                    matchlist_request = requests.get(f'https://{server}.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?endIndex=10&api_key={api}')
                except Exception:
                    traceback.print_exc()
                matchlist_json = matchlist_request.json()
                matchlist = matchlist_json['matches']
    
                last_wins = 0
                last_losses = 0
                kills = 0
                deaths = 0
                assists = 0
                participant_id = None
                
                for m in matchlist:
                    game_id = m['gameId']
                    champion_id = m['champion']
                    try:
                        game_request = requests.get(f'https://{server}.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={api}')
                    except Exception:
                        traceback.print_exc()
                    game_json = game_request.json()
                    
                    for pid in game_json['participantIdentities']:
                        try:
                            if pid['player']['summonerId'] == summoner_id:
                                participant_id = pid['participantId']
                        except:
                            if pid['player']['accountId'] == account_id:
                                participant_id = pid['participantId']

                    for p in game_json['participants']:
                        if p['participantId'] == participant_id:
                            kills += p['stats']['kills']
                            deaths += p['stats']['deaths']
                            assists += p['stats']['assists']
                            if p['stats']['win'] == True:
                                last_wins += 1
                            else:
                                last_losses += 1
            
                last_win_percentage = int((int(last_wins) / (int(last_wins) + int(last_losses))) * 100)
                average_kills = kills / 10
                average_deaths = deaths / 10
                average_assists = assists / 10 
                                
                try:
                    mastery_request = requests.get(f'https://{server}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api}')
                except Exception:
                    traceback.print_exc()
                mastery_json = mastery_request.json()
                
                champion_id = []
                champion_name = []
                champion_level = []
                champion_points = []
                
                for mastery in mastery_json[0:3]:
                    champion_id.append(mastery['championId'])
                    champion_level.append(mastery['championLevel'])
                    champion_points.append(mastery['championPoints'])
                for cid in champion_id:
                    with open(f'dragontail/{version}/data/en_GB/champion.json', encoding="utf8") as f:
                        champion = json.load(f)
                    for k,v in champion['data'].items():
                        if v['key'] == str(cid):
                            champion_name.append(v['name'])
                    f.close()
                    
                with open('data/champions.json', encoding='utf-8') as f:
                    emojis = json.load(f)
                for e in emojis:
                    if e['name'] == champion_name[0]:
                        mastery_uno_emoji = e['emoji']
                    if e['name'] == champion_name[1]:
                        mastery_dos_emoji = e['emoji']
                    if e['name'] == champion_name[2]:
                        mastery_tres_emoji = e['emoji']
                f.close()

                        
                try:        
                    league_request = requests.get(f'https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api}')
                except Exception:
                    traceback.print_exc()
                league_json = league_request.json()
                solo_tier = ''
                solo_rank = ''
                full_solo_rank = ''
                solo_wins = '0'
                solo_losses = '0'
                solo_lp = '0'
                solo_win_ratio = '0'
                flex_tier = ''         
                flex_rank = ''
                full_flex_rank = ''
                flex_wins = '0'
                flex_losses = '0'
                flex_lp = '0'
                flex_win_ratio = '0'
                solo_data = '**Unranked**'
                flex_data = '**Unranked**'
                    
                for l in league_json:
                    if l['queueType'] == 'RANKED_SOLO_5x5':
                        solo_tier = l['tier']
                        solo_rank = l['rank']
                        solo_wins = l['wins']
                        solo_losses = l['losses']
                        solo_lp = l['leaguePoints']
                        full_solo_rank = solo_tier + ' ' + solo_rank
                        with open('data/ranks.json') as f:
                            ranks = json.load(f)
                        solo_icon = ''
                        for rank in ranks:
                            if rank['id'].lower() == solo_tier.lower():
                                solo_icon = rank['emoji']
                        f.close()
                        solo_win_ratio = int((int(solo_wins) / (int(solo_wins) + int(solo_losses))) * 100)
                        solo_data = f'{solo_icon}**{full_solo_rank}** \n {solo_lp} LP / {solo_wins}W {solo_losses}L \n Win Ratio {solo_win_ratio}%'
                        
                        
                    if l['queueType'] == 'RANKED_FLEX_SR':
                        flex_tier = l['tier']
                        flex_rank = l['rank']
                        flex_wins = l['wins']
                        flex_losses = l['losses']
                        flex_lp = l['leaguePoints']
                        full_flex_rank = flex_tier + ' ' + flex_rank
                        flex_win_ratio = int((int(flex_wins) / (int(flex_wins) + int(flex_losses))) * 100)
                        with open('data/ranks.json') as f:
                            ranks = json.load(f)
                        flex_icon = ''
                        for rank in ranks:
                            if rank['id'].lower() == flex_tier.lower():
                                flex_icon = rank['emoji']
                        f.close()
                        flex_data = f'{flex_icon}**{full_flex_rank}** \n {flex_lp} LP / {flex_wins}W {flex_losses}L \n Win Ratio {flex_win_ratio}%'
                        
                try:
                    live_request = requests.get(f'https://{server}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={api}')
                except Exception:
                    traceback.print_exc()
                live_json = live_request.json()
                
                live_champion_id = None 
                live_champion_name = None
                queue_type = None
                live_data = ''
                champion_clear_name = None
                
                
                if live_request.status_code == 200:
                    for p in live_json['participants']:
                        if p['summonerId'] == summoner_id:
                            live_champion_id = p['championId']
                            with open(f'dragontail/{version}/data/en_GB/champion.json', encoding="utf8") as f:
                                champion = json.load(f)
                            for k,v in champion['data'].items():
                                if v['key'] == str(live_champion_id):
                                    live_champion_name = v['name']
                                    champion_clear_name = v['id']
                    with open('data/queues.json', encoding="utf8") as f:
                        queue = json.load(f)   
                    for q in queue:
                        if 'gameQueueConfigId' in live_json:
                            if q['queueId'] == live_json['gameQueueConfigId']:
                                queue_type = q['description']
                        else:
                            queue_type = 'Custom'
                    f.close()
                    with open('data/champions.json', encoding='utf-8') as f:
                        emojis = json.load(f)
                    for e in emojis:
                        if champion_clear_name == e['id']:
                            emoji = e['emoji']
                    f.close()
                    live_data = f'Playing a **{queue_type}** match as {emoji} **{live_champion_name}**.'
                else:
                    live_data = 'Not in an active game.'
                          
                    
                file = discord.File(f"{icon_full_path}", filename=f"{icon_png}")
                embed = discord.Embed(title=f"**{name}**'s Profile", color=0xfda5b0)
                embed.set_thumbnail(url=f'attachment://{icon_png}')
                embed.add_field(name='Region', value=f'{region.upper()} \n \u200B')
                embed.add_field(name='\u200B', value='\u200B')
                embed.add_field(name='Summoner Level', value=f'{level} \n \u200B')
                embed.add_field(name='Ranked (Solo/Duo)', value=f'{solo_data} \n \u200B')
                embed.add_field(name='\u200B', value='\u200B')
                embed.add_field(name='Ranked (Flex)', value=f'{flex_data} \n \u200B')
                embed.add_field(name='Recent 10 Games', value=f'{average_kills} / {average_deaths} / {average_assists} \n {last_wins}W {last_losses}L \n Win Ratio {last_win_percentage}% \n \u200B')
                embed.add_field(name='\u200B', value='\u200B')
                embed.add_field(name='Highest Champion Mastery', value=f'''
                                **[{champion_level[0]}]** {mastery_uno_emoji} {champion_name[0]}: {champion_points[0]:,}
                                **[{champion_level[1]}]** {mastery_dos_emoji} {champion_name[1]}: {champion_points[1]:,}
                                **[{champion_level[2]}]** {mastery_tres_emoji} {champion_name[2]}: {champion_points[2]:,}
                                \u200B''')
                embed.add_field(name='Live Game', value=live_data)
                await msg.edit(embed=embed) 
            except KeyError:
                embed=discord.Embed(description="Oops, Couldn't find summoner!", color=0xfda5b0)
                await ctx.send(embed=embed)       
            except Exception:
                traceback.print_exc()
                except_embed = discord.Embed(description=f"Something went wrong, couldn't fetch {name}'s data.", color=0xfda5b0)
                except_embed.set_thumbnail(url=f'attachment://{icon_png}')
                await msg.edit(embed=except_embed)
           
    
    @commands.command()
    async def history(self, ctx, region=None, *, summoner=None):
        regions = ['euw', 'br', 'na', 'eune', 'jp', 'las', 'lan', 'oce', 'tr', 'kr', 'ru']
        servers = {'euw':'euw1','br':'br1', 'na':'na1', 'eune':'eun1', 'jp':'jp1', 'las':'la2', 'lan':'la1', 'oce':'oc1', 'tr':'tr1', 'kr':'kr', 'ru':'ru'}
        if region is None and summoner is None:
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
                if data is not None:
                    profile_data = list(data)
                    region = profile_data[1]
                    summoner = profile_data[2]
                    await self.history(ctx, region, summoner=summoner)
                else:
                    embed=discord.Embed(title=f'{ops} Seraphine: History', description="You dont have a summoner added. \n \u200B \n Add your profile so you don't have to specify your account information!", color=0xfda5b0)
                    embed.add_field(name='Add Your Summoner', value='`!add [region] [summoner]`')
                    embed.add_field(name='Specify', value='`!history [region] [summoner]`')
                    await ctx.send(embed=embed)
                cur.close()
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
            else:
                if conn is not None:
                    conn.close()
                    
        elif region.lower() not in regions:
            embed=discord.Embed(title=f'{ops} Seraphine: History', description="Invalid region!", color=0xfda5b0)
            embed.add_field(name='Regions', value='`br` `eune` `euw` `jp` `kr` `lan` `las` `na` `oce` `ru` `tr`')
            await ctx.send(embed=embed)  
        elif summoner is None:
            embed=discord.Embed(title=f'{ops} Seraphine: History', description="You're missing something!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!history [region] [summoner]`')
            await ctx.send(embed=embed) 
        else:
            for k,v in servers.items():
                if region.lower() == k:
                    server = v
            try:
                try:
                    summoner_request = requests.get(f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api}')
                except Exception:
                    traceback.print_exc()
                summoner_json = summoner_request.json()
                account_id = summoner_json['accountId']
                icon_id = summoner_json['profileIconId']
                name = summoner_json['name']
                
                try:
                    matchlist_request = requests.get(f'https://{server}.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?endIndex=10&api_key={api}')
                except Exception:
                    traceback.print_exc()
                matchlist_json = matchlist_request.json()
                matchlist = matchlist_json['matches']
                
                with open(f'dragontail/{version}/data/en_GB/profileicon.json') as f:
                    icon = json.load(f)
                icon_path = f'dragontail/{version}/img/profileicon/'
                icon_png = icon['data'][f'{icon_id}']['image']['full']
                icon_full_path = icon_path + icon_png
                f.close()
                
                file = discord.File(f"{icon_full_path}", filename=f"{icon_png}")
                embed = discord.Embed(title=f"**{name}**'s Match History", description='', color=0xfda5b0) 
                embed.set_thumbnail(url=f'attachment://{icon_png}')
                
                temp_embed = discord.Embed(description=f"Fetching {name}'s match history, wait a moment...", color=0xfda5b0)
                temp_embed.set_thumbnail(url=f'attachment://{icon_png}')
                msg = await ctx.send(embed=temp_embed, file=file)
                
                champion_name = None
                game_id = None
                champion_id = None
                icon_id = None
                kills = None
                deaths = None
                assists = None
                win = '<:win:828195734841983037>'
                loss = '<:loss:828195062700834826>'
                status = None
                minions = None
                gold = None
                queue_type = None
                participant_id = None
                champion_clear_name = None
                
                for m in matchlist:
                    game_id = m['gameId']
                    champion_id = m['champion']                  
                    
                    with open(f'dragontail/{version}/data/en_GB/champion.json', encoding="utf8") as f:
                        champion = json.load(f)
                    for k,v in champion['data'].items():
                        if v['key'] == f'{champion_id}':
                            champion_name = v['name']
                            champion_clear_name = v['id']
                    f.close()
                    with open('data/champions.json', encoding='utf-8') as f:
                        emojis = json.load(f)
                    for e in emojis:
                        if champion_clear_name == e['id']:
                            emoji = e['emoji']
                    f.close()
                    try:
                        game_request = requests.get(f'https://{server}.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={api}')
                    except Exception:
                        traceback.print_exc()
                    game_json = game_request.json()
                    
                    for pid in game_json['participantIdentities']:
                        if pid['player']['accountId'] == account_id:
                            participant_id = pid['participantId']
                    
                    with open('data/queues.json', encoding="utf8") as f:
                        queue = json.load(f)   
                    for q in queue:
                        if q['queueId'] == game_json['queueId']:
                            description = q['description']
                            queue_type = description
                    f.close()
                                                
                    for p in game_json['participants']:
                        if p['participantId'] == participant_id:
                            kills = p['stats']['kills']
                            deaths = p['stats']['deaths']
                            assists = p['stats']['assists']
                            status = win if p['stats']['win'] == True else loss
                            minions = p['stats']['totalMinionsKilled']
                            gold = p['stats']['goldEarned']
                    embed.add_field(name=f'{status} {emoji} {champion_name} - ({queue_type})', value=f'''{kills} / {deaths} / {assists} \u200B \u200B <:minion:823209384908816404>{minions} \u200B \u200B <:gold:823209384942370836>{gold}''', inline=False)
                await msg.edit(embed=embed) 
            except KeyError:
                embed=discord.Embed(description="Oops, Couldn't find summoner!", color=0xfda5b0)
                await ctx.send(embed=embed)
            except Exception:
                traceback.print_exc()
                except_embed = discord.Embed(description=f"Something went wrong, couldn't fetch {name}'s data.", color=0xfda5b0)
                except_embed.set_thumbnail(url=f'attachment://{icon_png}')
                await msg.edit(embed=except_embed)           
            
    
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
        
    # @commands.command()
    # async def live(self, ctx, region, *, summoner):
    #     regions = ['euw', 'br', 'na', 'eun', 'jp', 'la', 'oc', 'tr', 'kr', 'ru']
    #     regionwithones = ['euw', 'br', 'na', 'eun', 'jp', 'la', 'oc', 'tr']
    #     server = region

    #     if region not in regions:
    #         embed=discord.Embed(description="Invalid region!", color=0xfda5b0)
    #         embed.add_field(name='Regions', value='`euw` `br` `na` `eun` `jp` `la` `oc` `tr` `kr` `ru`')
    #         await ctx.send(embed=embed) 
    #     else:
    #         if region in regionwithones:
    #             server = server + '1'
    #         try:
    #             summoner_request = requests.get(f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api}')
    #             if summoner_request.status_code == 404:
    #                 await ctx.send("Oops, Couldn't find summoner.")
    #         except Exception:
    #             traceback.print_exc()
    #         summoner_json = summoner_request.json()
    #         summoner_id = summoner_json['id']
            
    #         try:
    #             live_request = requests.get(f'https://{server}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={api}')
    #         except Exception:
    #             traceback.print_exc()
    #         live_json = live_request.json()
            
    #         queue_type = None
    #         live_data = ''
    #         team_one = []
    #         team_one_champs = []
            
    #         team_two = []
    #         team_two_champs = []
            
    #         if live_request.status_code == 200:
    #             for p in live_json['participants']:
    #                 if p['teamId'] == 100:
    #                     team_one_summoners = (p['summonerName'])
    #                     team_one_ids = (p['championId'])\
    #                     dic = {team_one_summoners: team_one_ids}
    #                     team_one.append(dic)
    #                 else:
    #                     team_two_summoners = (p['summonerName'])
    #                     team_two_ids = (p['championId'])
    #                     team_two.update({team_two_summoners: team_two_ids})
    #             print(team_one)
                                   
                        
    #             with open(f'dragontail/{version}/data/en_GB/champion.json', encoding="utf8") as f:
    #                 champion = json.load(f)
                        
    #             for k,v in champion['data'].items():
    #                 for ids in team_one.values:
    #                     if v['key'] == str(ids):
    #                         team_one_champs.append(v['name'])
    #                 for ids in team_two.values:
    #                     if v['key'] == str(ids):
    #                         team_two_champs.append(v['name']) 
                                    
    #             with open('data/queues.json', encoding="utf8") as f:
    #                 queue = json.load(f)   
    #             for q in queue:
    #                 if 'gameQueueConfigId' in live_json:
    #                     if q['queueId'] == live_json['gameQueueConfigId']:
    #                         queue_type = q['description']
    #                 else:
    #                     queue_type = 'Custom'
    #             f.close()
    #             # embed=discord.Embed(title=f"{queue_type}", color=0xfda5b0)
    #             # embed.add_field(name='Blue Team', value=f"""
    #             #     [{team_one_champs[0]}]\t**{team_one_names[0]}**
    #             #     [{team_one_champs[1]}]\t**{team_one_names[1]}**
    #             #     [{team_one_champs[2]}]\t**{team_one_names[2]}**
    #             #     [{team_one_champs[3]}]\t**{team_one_names[3]}**
    #             #     [{team_one_champs[4]}]\t**{team_one_names[4]}**""")
    #             # embed.add_field(name='Rank', value="""
    #             #                 rank
    #             #                 rank
    #             #                 rank
    #             #                 rank
    #             #                 rank
    #             #                 """)
    #             # embed.add_field(name='Ranked WR', value="""
    #             #                 100% 40G
    #             #                 100% 40G
    #             #                 100% 40G
    #             #                 100% 40G
    #             #                 100% 40G
    #             #                 """)
                
    #             # embed.add_field(name='Red Team', value=f"""
    #             #     [{team_two_champs[0]}]\t**{team_two_names[0]}**
    #             #     [{team_two_champs[1]}]\t**{team_two_names[1]}**
    #             #     [{team_two_champs[2]}]\t**{team_two_names[2]}**
    #             #     [{team_two_champs[3]}]\t**{team_two_names[3]}**
    #             #     [{team_two_champs[4]}]\t**{team_two_names[4]}**""")
    #             # embed.add_field(name='Rank', value="""
    #             #                 rank
    #             #                 rank
    #             #                 rank
    #             #                 rank
    #             #                 rank
    #             #                 """)
    #             # embed.add_field(name='Ranked WR', value="""
    #             #                 100% 40G
    #             #                 100% 40G
    #             #                 100% 40G
    #             #                 100% 40G
    #             #                 100% 40G
    #             #                 """)
    #             # await ctx.send(embed=embed)
    #         else:
    #             live_data = 'Not in an active game.'
    #             embed = discord.Embed(description={live_data}, color=0xfda5b0)
                
                           
def setup(client):
    client.add_cog(League(client))