import discord
from discord.ext import commands
import requests
import json

api = 'RGAPI-75ccb4b5-e9aa-486d-99aa-23ca507dd270'
version = '11.6.1'
                
class League(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def profile(self, ctx, server, *, summoner):
        if server == 'euw' or server == 'br' or server == 'na' or server == 'eun' or server == 'jp' or server == 'la' or server == 'oc' or server == 'tr' or server == 'kr' or server == 'ru':
            if server == 'euw' or server == 'br' or server == 'na' or server == 'eun' or server == 'jp' or server == 'la' or server == 'oc' or server == 'tr':
                server = server + '1'
            try:
                summoner_request = requests.get(f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api}')
            except Exception as e:
                print('Summoner request: ', e)
            summoner_json = summoner_request.json()
            summoner_id = summoner_json['id']
            name = summoner_json['name']
            level = summoner_json['summonerLevel']
            icon_id = summoner_json['profileIconId']
                
            try:        
                league_request = requests.get(f'https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api}')
            except Exception as e:
                print('League request: ', e)
            league_json = league_request.json()
            solo_tier = None
            solo_rank = None
            full_solo_rank = 'Unranked'
            solo_wins = '0'
            solo_losses = '0'
            solo_lp = '0'
            solo_win_ratio = '0'
            flex_tier = None         
            flex_rank = None
            full_flex_rank = 'Unranked'
            flex_wins = '0'
            flex_losses = '0'
            flex_lp = '0'
            flex_win_ratio = '0'
                
            for l in league_json:
                if l['queueType'] == 'RANKED_SOLO_5x5':
                    solo_tier = l['tier']
                    solo_rank = l['rank']
                    solo_wins = l['wins']
                    solo_losses = l['losses']
                    solo_lp = l['leaguePoints']
                    full_solo_rank = solo_tier + ' ' + solo_rank
                    solo_win_ratio = int((int(solo_wins) / (int(solo_wins) + int(solo_losses))) * 100)
                    
                if l['queueType'] == 'RANKED_FLEX_SR':
                    flex_tier = l['tier']
                    flex_rank = l['rank']
                    flex_wins = l['wins']
                    flex_losses = l['losses']
                    flex_lp = l['leaguePoints']
                    full_flex_rank = flex_tier + ' ' + flex_rank
                    flex_win_ratio = int((int(flex_wins) / (int(flex_wins) + int(flex_losses))) * 100)
                    
                
            with open(f'dragontail\\{version}\\data\\en_GB\\profileicon.json') as f:
                icon = json.load(f)
            icon_path = f'dragontail\\{version}\\img\\profileicon\\'
            icon_png = icon['data'][f'{icon_id}']['image']['full']
            icon_full_path = icon_path + icon_png
            f.close()
                
            file = discord.File(f"{icon_full_path}", filename=f"{icon_png}")
            embed = discord.Embed(title=f'**{name}** - Summoner Level: {level}')
            embed.set_thumbnail(url=f'attachment://{icon_png}')
            embed.add_field(name='Ranked (Solo/Duo)', value=f'{full_solo_rank} \n {solo_lp} LP / {solo_wins}W {solo_losses}L \n Win Ratio {solo_win_ratio}%')
            embed.add_field(name='Ranked (Flex)', value=f'{full_flex_rank} \n {flex_lp} LP / {flex_wins}W {flex_losses}L \n Win Ratio {flex_win_ratio}%')
            await ctx.send(file=file, embed=embed)          
        else:
            await ctx.send("Invalid League of Legends server.")
    
    @commands.command()
    async def history(self, ctx, server, *, summoner):
        if server == 'euw' or server == 'br' or server == 'na' or server == 'eun' or server == 'jp' or server == 'la' or server == 'oc' or server == 'tr' or server == 'kr' or server == 'ru':
            if server == 'euw' or server == 'br' or server == 'na' or server == 'eun' or server == 'jp' or server == 'la' or server == 'oc' or server == 'tr':
                server = server + '1'
            try:
                summoner_request = requests.get(f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api}')
            except Exception as e:
                print('Summoner request: ', e)
            summoner_json = summoner_request.json()
            account_id = summoner_json['accountId']
            icon_id = summoner_json['profileIconId']
            name = summoner_json['name']
            
            try:
                matchlist_request = requests.get(f'https://{server}.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?endIndex=5&api_key={api}')
            except Exception as e:
                print('Match list request: ', e)
            matchlist_json = matchlist_request.json()
            matchlist = matchlist_json['matches']
            
            embed = discord.Embed(title=f'**{name}** - Match History', description='')
            with open(f'dragontail\\{version}\\data\\en_GB\\profileicon.json') as f:
                icon = json.load(f)
            icon_path = f'dragontail\\{version}\\img\\profileicon\\'
            icon_png = icon['data'][f'{icon_id}']['image']['full']
            icon_full_path = icon_path + icon_png
            f.close()
            file = discord.File(f"{icon_full_path}", filename=f"{icon_png}") 
            embed.set_thumbnail(url=f'attachment://{icon_png}')
            
            champion_name = None
            game_id = None
            champion_id = None
            icon_id = None
            kills = None
            deaths = None
            assists = None
            win = '<:win:823293769544630323>'
            loss = '<:defeat:823294088559984660>'
            status = None
            minions = None
            gold = None
            queue_type = None
            
            for m in matchlist:
                game_id = m['gameId']
                champion_id = m['champion']                  
                
                with open(f'dragontail\\{version}\\data\\en_GB\\champion.json', encoding="utf8") as f:
                    champion = json.load(f)
                for k,v in champion['data'].items():
                    if v['key'] == f'{champion_id}':
                        champion_name = v['name']
                f.close()
                try:
                    game_request = requests.get(f'https://{server}.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={api}')
                except Exception as e:
                    print(e)
                game_json = game_request.json()
                
                with open(f'dragontail\\11.6.1\\data\\en_GB\\queues.json', encoding="utf8") as f:
                    queue = json.load(f)   
                for q in queue:
                    if q['queueId'] == game_json['queueId']:
                        description = q['description']
                        queue_type = description
                f.close()                    
                    
                for p in game_json['participants']:
                    if p['championId'] == champion_id:
                        kills = p['stats']['kills']
                        deaths = p['stats']['deaths']
                        assists = p['stats']['assists']
                        status = win if p['stats']['win'] == True else loss
                        minions = p['stats']['totalMinionsKilled']
                        gold = p['stats']['goldEarned']
                embed.add_field(name=f'{status} {champion_name} - ({queue_type})', value=f'''{kills} / {deaths} / {assists} \u200B \u200B <:minion:823209384908816404>{minions} \u200B \u200B <:gold:823209384942370836>{gold} \n \u200B''', inline=False)
            await ctx.send(file=file, embed=embed)
    
def setup(client):
    client.add_cog(League(client))