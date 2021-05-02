import discord
from discord.ext import commands
import requests
import json
import traceback
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio

load_dotenv()
api = str(os.getenv('API_KEY'))
version = str(os.getenv('VERSION'))

host = str(os.getenv('HOST'))
database = str(os.getenv('DATABASE'))
user = str(os.getenv('USER'))
password = str(os.getenv('PASSWORD'))
port = str(os.getenv('PORT'))

ops = '<:outage:835522354963677184>'
check = '<:check:835842893696204830>'
sep = '<:sep:838164218514505759>'
                
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
                puuid = summoner_json['puuid']
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
                    
                with open('data/championIcons.json', encoding='utf-8') as f:
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
                    with open('data/championIcons.json', encoding='utf-8') as f:
                        emojis = json.load(f)
                    for e in emojis:
                        if champion_clear_name == e['id']:
                            emoji = e['emoji']
                    f.close()
                    live_data = f'Playing a **{queue_type}** match as {emoji} **{live_champion_name}**.'
                else:
                    live_data = 'Not in an active game.'
                          
                    
                file = discord.File(f"{icon_full_path}", filename=f"{icon_png}")
                embed = discord.Embed(description=f"Summary of the profile you asked for: \n \u200B", color=0xfda5b0)
                embed.set_author(name=f'Profile: {name} [{region.upper()}]', icon_url=f'attachment://{icon_png}')
                embed.add_field(name='Summoner Level', value=f'{level} \n \u200B')
                embed.add_field(name='\u200B', value='\u200B')
                embed.add_field(name='\u200B', value='\u200B')
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
                embed = discord.Embed(description=f"Recent Games (Last 10 Played): \n \u200B", color=0xfda5b0)
                embed.set_author(name=f'Match History: {name} [{region.upper()}]', icon_url=f'attachment://{icon_png}')
                
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
                    with open('data/championIcons.json', encoding='utf-8') as f:
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
                    embed.add_field(name=f'{status} {emoji} {champion_name} - ({queue_type})', value=f'''<:kda:838239099822669824>{kills} / {deaths} / {assists} \u200B \u200B <:minion:823209384908816404>{minions} \u200B \u200B <:gold:823209384942370836>{gold}''', inline=False)
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
    async def mastery(self, ctx, region=None, summoner=None):
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
                    await self.mastery(ctx, region, summoner=summoner)
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
                icon_id = summoner_json['profileIconId']
                masteryScore_request = requests.get(f'https://{server}.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{summoner_id}?api_key={api}')
                championMasteryList_request = requests.get(f'https://{server}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api}')
                championMasteryList = championMasteryList_request.json()
                
                with open(f'dragontail/{version}/data/en_GB/profileicon.json') as f:
                    icon = json.load(f)
                icon_path = f'dragontail/{version}/img/profileicon/'
                icon_png = icon['data'][f'{icon_id}']['image']['full']
                icon_full_path = icon_path + icon_png
                f.close()
                
                nl = '\n'
                chestTrue = '<:chest:837893366116909076>'
                chestFalse = '<:nochest:837895944317698069>'
                blank = '<:BLANK:837828544410550282>'
                
                totalMasteryScore = masteryScore_request.json()
                masteryPoints = 0
                chestsGained = 0
                championsCount = len(championMasteryList)
                champions = []

                for m in championMasteryList[:10]:
                    level = m['championLevel']
                    id = m['championId']
                    points = m['championPoints']
                    lastplayed = m['lastPlayTime']
                    chest = m['chestGranted']
                    tokens = m['tokensEarned']
                    champions.append([level,id,points,lastplayed,chest,tokens])

                for m in championMasteryList:
                    masteryPoints += m['championPoints']
                    
                for m in championMasteryList:
                    if m['chestGranted'] is True:
                        chestsGained += 1

                with open('data/championIcons.json', encoding='utf-8') as f:
                    champs = json.load(f)

                with open('data/mastery.json', encoding='utf-8') as k:
                    mastery = json.load(k)

                championListOrganized = []
                
                for c in champions:
                    if c[4] is False:
                        c[4] = chestFalse
                    else:
                        c[4] = chestTrue
                    
                    if c[0] == 7:
                        c[5] = 'Mastered'
                    else:
                        c[5] = str(c[5]) + ' Tokens'


                    for i in champs:
                        if str(c[1]) == i['key']:
                            c[1] = i['emoji'] + ' ' + i['name']
                    for i in mastery:
                        if c[0] == i['mastery']:
                            c[0] = i['emoji']

                    convert = c[3] / 1000
                    temp = datetime.fromtimestamp(convert).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    then = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S.%fZ")
                    now = datetime.now()
                    seconds = (now-then).total_seconds()
                    minutes = seconds / 60
                    hours = minutes / 60
                    days = hours / 24
                    weeks = days / 7
                    months = weeks * 0.229984

                    if seconds < 120:
                        c[3] = blank + str(int(minutes)) + ' minute ago'
                    elif seconds < 3600:
                        c[3] = blank + str(int(minutes)) + ' minutes ago'
                    elif seconds < 7200:
                        c[3] = blank + str(int(hours)) + ' hour ago'
                    elif seconds < 86400:
                        c[3] = blank + str(int(hours)) + ' hours ago'
                    elif seconds < 172800:
                        c[3] = blank + str(int(days)) + ' day ago'
                    elif seconds < 604800:
                        c[3] = blank + str(int(days)) + ' days ago'
                    elif seconds < 1210000:
                        c[3] = blank + str(int(weeks)) + ' week ago'
                    elif seconds < 2628000:
                        c[3] = blank + str(int(weeks)) + ' weeks ago'
                    elif seconds < 5256000:
                        c[3] = blank + str(int(months)) + ' month ago'
                    else:
                        c[3] = blank + str(int(months)) + ' months ago'
                    
                    first = c[0] + ' **' + c[1] + '**' + ' - ' + f'{c[2]:,}'
                    second = c[3]
                    third = c[4] + ' - ' + c[5]
                    championListOrganized.append([first,second,third])
                
                file = discord.File(f"{icon_full_path}", filename=f"{icon_png}")
                embed = discord.Embed(description='Champions with the highest mastery points: \n \u200B', color=0xfda5b0)
                embed.set_author(name=f'Mastery: {summoner} [{region}]', icon_url=f"attachment://{icon_png}")
                embed.add_field(name='Champion Mastery', value=f"{f'{nl}'.join([c[0] for c in championListOrganized])}")
                embed.add_field(name=f'{blank}Last Played', value=f"{f'{nl}'.join([c[1] for c in championListOrganized])}")
                embed.add_field(name='Chest/Status', value=f"{f'{nl}'.join([c[2] for c in championListOrganized])}")
                embed.add_field(name='\u200B', value=f"**Champions:** {championsCount} · **Mastery Score:** {totalMasteryScore} · **Mastery Points:** {masteryPoints:,} · **Chests Gained:** {chestsGained}/{championsCount}")
                await ctx.send(file=file, embed=embed)
            except KeyError:
                embed=discord.Embed(description="Oops, Couldn't find summoner!", color=0xfda5b0)
                await ctx.send(embed=embed)
            except Exception:
                traceback.print_exc()
    
    @commands.command()
    async def rotation(self, ctx):
        r = requests.get(f'https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={api}')
        rotation_json = r.json()
        
        temp = []
        champion_names = []        
        with open(f'dragontail/{version}/data/en_GB/champion.json', encoding="utf8") as f:
            champion = json.load(f)
        for p in rotation_json['freeChampionIds']:
            for k,v in champion['data'].items():
                if v['key'] == str(p):
                    temp.append(v['name'])
        f.close()   
        
        with open('data/championIcons.json', encoding='utf-8') as f:
                emojis = json.load(f)
        for e in emojis:
            for c in temp:
                if e['name'] == c:
                    emoji = e['emoji']
                    newstring = emoji + ' ' + c
                    champion_names.append(newstring)
        f.close()
        nl = '\n'
        
        embed = discord.Embed(title='Champion Rotations',description=f"This week's free rotation:", color=0xfda5b0)
        embed.set_thumbnail(url='https://seraphine-bot.s3.eu-central-1.amazonaws.com/lol_icon_32.png')
        embed.add_field(name='\u200B', value=f"**{f'{nl}'.join([c for c in champion_names[:10]])}**")
        embed.add_field(name='\u200B', value=f"**{f'{nl}'.join([c for c in champion_names[10:]])}**")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def rankings(self, ctx, region=None):
        regions = ['euw', 'br', 'na', 'eune', 'jp', 'las', 'lan', 'oce', 'tr', 'kr', 'ru']
        servers = {'euw':'euw1','br':'br1', 'na':'na1', 'eune':'eun1', 'jp':'jp1', 'las':'la2', 'lan':'la1', 'oce':'oc1', 'tr':'tr1', 'kr':'kr', 'ru':'ru'}
        if region is None:
            embed=discord.Embed(title=f'{ops} Seraphine: Rankings', description="You're missing something!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!rankings [region]`')
            await ctx.send(embed=embed)                  
        elif region.lower() not in regions:
            embed=discord.Embed(title=f'{ops} Seraphine: Rankings', description="Invalid region!", color=0xfda5b0)
            embed.add_field(name='Regions', value='`br` `eune` `euw` `jp` `kr` `lan` `las` `na` `oce` `ru` `tr`')
            await ctx.send(embed=embed)
        else:
            for k,v in servers.items():
                if region.lower() == k:
                    server = v
            try:
                leagueEntries_request = requests.get(f'https://{server}.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&api_key={api}')
            except Exception:
                traceback.print_exc()
                
            entryList = leagueEntries_request.json()
            blank = '<:BLANK:837828544410550282>'
            nl = '\n'
            summoners = []
            buttons = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            current = 0
            
            i = 1
            for e in entryList[:100]:
                summonerName =  f'{i}. ' + e['summonerName'] + blank
                rank = blank + e['tier'] + ' ' + str(e['leaguePoints']) + ' LP'
                wins = e['wins']
                losses = e['losses']
                winrate = int((int(wins) / (int(wins) + int(losses))) * 100)
                winsall = blank + '**Wins: ' + str(wins) + '** · ' + str(winrate) + '% WR'
                summoners.append([summonerName, rank, winsall])
                i += 1               
            
            page1 = discord.Embed (
                title = f'Seraphine: Rankings',
                description = f'Top Players Rankings in {region.upper()}: \n \u200B',
                colour = 0xfda5b0
            ).add_field(name=f'Name', value=f"**{f'{nl}'.join([s[0] for s in summoners[:20]])}**").add_field(name=f'{blank}Solo Queue', value=f"**{f'{nl}'.join([s[1] for s in summoners[:20]])}**").add_field(name='\u200B', value=f"{f'{nl}'.join([s[2] for s in summoners[:20]])}")
            page2 = discord.Embed (
                 title = f'Seraphine: Rankings',
                description = f'Top Players Rankings in {region.upper()}: \n \u200B',
                colour = 0xfda5b0
            ).add_field(name=f'Name', value=f"**{f'{nl}'.join([s[0] for s in summoners[20:40]])}**").add_field(name=f'{blank}Solo Queue', value=f"**{f'{nl}'.join([s[1] for s in summoners[20:40]])}**").add_field(name='\u200B', value=f"{f'{nl}'.join([s[2] for s in summoners[20:40]])}")
            page3 = discord.Embed (
                 title = f'Seraphine: Rankings',
                description = f'Top Players Rankings in {region.upper()}: \n \u200B',
                colour = 0xfda5b0
            ).add_field(name=f'Name', value=f"**{f'{nl}'.join([s[0] for s in summoners[40:60]])}**").add_field(name=f'{blank}Solo Queue', value=f"**{f'{nl}'.join([s[1] for s in summoners[40:60]])}**").add_field(name='\u200B', value=f"{f'{nl}'.join([s[2] for s in summoners[40:60]])}")
            page4 = discord.Embed (
                 title = f'Seraphine: Rankings',
                description = f'Top Players Rankings in {region.upper()}: \n \u200B',
                colour = 0xfda5b0
            ).add_field(name=f'Name', value=f"**{f'{nl}'.join([s[0] for s in summoners[60:80]])}**").add_field(name=f'{blank}Solo Queue', value=f"**{f'{nl}'.join([s[1] for s in summoners[60:80]])}**").add_field(name='\u200B', value=f"{f'{nl}'.join([s[2] for s in summoners[60:80]])}")
            page5 = discord.Embed (
                title = f'Seraphine: Rankings',
                description = f'Top Players Rankings in {region.upper()}: \n \u200B',
                colour = 0xfda5b0
            ).add_field(name=f'Name', value=f"**{f'{nl}'.join([s[0] for s in summoners[80:100]])}**").add_field(name=f'{blank}Solo Queue', value=f"**{f'{nl}'.join([s[1] for s in summoners[80:100]])}**").add_field(name='\u200B', value=f"{f'{nl}'.join([s[2] for s in summoners[80:100]])}")

            pages = [page1, page2, page3, page4, page5]

            msg = await ctx.send(embed=pages[current].set_footer(text=f"Page {current+1}ᅠ•ᅠNavigate through the rankings using the reactions below!").set_thumbnail(url='https://seraphine-bot.s3.eu-central-1.amazonaws.com/lol_icon_32.png'))

            for button in buttons:
                await msg.add_reaction(button)
                
            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons and reaction.message.id == msg.id, timeout=30.0)

                except asyncio.TimeoutError:
                    pass

                else:
                    previous_page = current
                    if reaction.emoji == "1️⃣":
                        current = 0
                        await msg.remove_reaction("1️⃣", ctx.author)
                        
                    elif reaction.emoji == "2️⃣":
                        current = 1
                        await msg.remove_reaction("2️⃣", ctx.author)
                            
                    elif reaction.emoji == "3️⃣":
                        current = 2
                        await msg.remove_reaction("3️⃣", ctx.author)

                    elif reaction.emoji == "4️⃣":
                        current = 3
                        await msg.remove_reaction("4️⃣", ctx.author)
                        
                    elif reaction.emoji == "5️⃣":
                        current = 4
                        await msg.remove_reaction("5️⃣", ctx.author)

                    if current != previous_page:
                        await msg.edit(embed=pages[current].set_footer(text=f"Page {current+1}ᅠ•ᅠNavigate through the rankings using the reactions below!").set_thumbnail(url='https://seraphine-bot.s3.eu-central-1.amazonaws.com/lol_icon_32.png'))
            
                                                          
                           
def setup(client):
    client.add_cog(League(client))