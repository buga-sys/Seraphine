import discord
from discord.ext import commands
import json
import re
import traceback
import asyncio
import os
from dotenv import load_dotenv
import requests
import bs4

load_dotenv()
version = str(os.getenv('VERSION'))
api = str(os.getenv('API_KEY'))

ops = '<:outage:835522354963677184>'

class Champions(commands.Cog):
    def __init__(self, client):
        self.client = client   
   
    @commands.command()
    async def champion(self, ctx, value):
        if len(value) > 2:
            try:
                
                roles = [
                {
                    "name":'Tank',
                    "icon": '<:tank:837492725518565387>'
                 },
                {
                    "name":'Support',
                    "icon": '<:support:837492725820817448>'
                 },
                {
                    "name":'Marksman',
                    "icon": '<:marksman:837492725740863508>'
                 },
                {
                    "name":'Mage',
                    "icon": '<:mage1:837492725661302815>'
                 },
                {
                    "name":'Fighter',
                    "icon": '<:fighter:837492725632335892>'
                 },
                {
                    "name":'Assassin',
                    "icon": '<:assassin:837492725858566174>'
                 }
                ]
                
                with open(f'dragontail/{version}/data/en_GB/championFull.json', encoding='utf-8') as f:
                    champions = json.load(f)
                
                champions_data = champions['data']
                champion = value.lower()
                name = None
                title = None
                tags = []
                partype = None
                spells_names = []
                spells_description = []
                images_path = f'dragontail/{version}/img/champion/'
                champion_image = None
                passive_name = None
                passive_description = None

                for k,v in champions_data.items():
                    if champion == v['name'].lower() or champion == k.lower():
                        name = v['name']
                        title = v['title']
                        champion_image = v['image']['full']
                        partype = v['partype']
                        for tag in v['tags']:
                            for r in roles:
                                if tag == r['name']:
                                    tags.append(r['icon'])
                        for spell in v['spells']:
                            spells_names.append(spell['name'])
                            clean = re.compile('<.*?>')
                            description = re.sub(clean, "", spell['description'])  
                            spells_description.append(description)
                        passive_name = v['passive']['name']
                        passive_description = v['passive']['description']
                        clean = re.compile('<.*?>')
                        passive_description = re.sub(clean, "", passive_description)
                image_full_path = images_path + champion_image
                f.close()
                
                file = discord.File(f"{image_full_path}", filename=f"{champion_image}")
                embed = discord.Embed(title=f'{name} - {title.title()}', description=f'''{' '.join(tags)} \n Partype: {partype}''', color=0xfda5b0)
                embed.set_thumbnail(url=f'attachment://{champion_image}')
                embed.add_field(name=f'(Passive) {passive_name}', value=f"{passive_description}", inline=False)
                embed.add_field(name=f'(Q) {spells_names[0]}', value=f"{spells_description[0]}", inline=False)
                embed.add_field(name=f'(W) {spells_names[1]}', value=f"{spells_description[1]}", inline=False)
                embed.add_field(name=f'(E) {spells_names[2]}', value=f"{spells_description[2]}", inline=False)
                embed.add_field(name=f'(R) {spells_names[3]}', value=f"{spells_description[3]}", inline=False)
                await ctx.send(file=file, embed=embed)
            except TypeError:
                embed=discord.Embed(title=f'{ops} Seraphine: Champion', description="That's not a valid champion's name!", color=0xfda5b0)
                await ctx.send(embed=embed) 
            except Exception:
                traceback.print_exc()
        else:
            embed=discord.Embed(title=f'{ops} Seraphine: Champion', description="That's not a valid champion's name!", color=0xfda5b0)
            await ctx.send(embed=embed) 
    
    @champion.error
    async def champion_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(title=f'{ops} Seraphine: Champion', description="You need to give me a champion!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!champion [champion]`')
            await ctx.send(embed=embed) 
            
    @commands.command()
    async def skins(self, ctx, champion):
        try:
            with open(f'lolstaticdata/champions.json', encoding='utf-8') as f:
                champions = json.load(f)

            name = None
            rarity = None
            cost = None
            rp = '<:rp:838109393307697184>'
            pages = []
            buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
            current = 0
            skinRarity = [
                {
                    "name":'Epic',
                    "icon": '<:Epic_Skin:837722859866030201>'
                 },
                {
                    "name":'Mythic',
                    "icon": '<:Mythic_Skin:837722860277071902>'
                 },
                {
                    "name":'Legendary',
                    "icon": '<:Legendary_Skin:837722860248236072>'
                 },
                {
                    "name":'Ultimate',
                    "icon": '<:Ultimate_Skin:837722843188953118>'
                 },
                {
                    "name":'NoRarity',
                    "icon": ''
                 }
            ]
        
            
            for k,v in champions.items():
                if champion.lower() == v['name'].lower() or champion.lower() == k.lower():
                    cid = v['name']
                    picid = v['key']
                    for c in v['skins'][1:]:
                        name = c['name']
                        if c['cost'] == 'special':
                            cost = c['distribution']
                        else:
                            cost = rp + ' ' + str(c['cost'])
                        rarity = c['rarity']
                        for r in skinRarity:
                            if r['name'] == rarity:
                                rarity = r['icon']
                        imageurl = c['loadScreenPath']
                        page = discord.Embed(description="Here's what you asked for: \n \u200B", color=0xfda5b0).add_field(name=f'{rarity} {name}',value=f'{cost}').set_image(url=imageurl).set_author(name=f'{cid} Skins', icon_url=f'https://seraphine-bot.s3.eu-central-1.amazonaws.com/champion/{picid}.png')
                        pages.append(page)    
            f.close()
            
            msg = await ctx.send(embed=pages[current].set_footer(text=f"{current+1}/{len(pages)}"))
            
            for button in buttons:
                await msg.add_reaction(button)
                
            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons and reaction.message.id == msg.id, timeout=30.0)

                except asyncio.TimeoutError:
                    pass

                else:
                    previous_page = current
                    if reaction.emoji == u"\u23EA":
                        current = 0
                        await msg.remove_reaction(u"\u23EA", ctx.author)
                        
                    elif reaction.emoji == u"\u2B05":
                        if current > 0:
                            current -= 1
                        await msg.remove_reaction(u"\u2B05", ctx.author)
                            
                    elif reaction.emoji == u"\u27A1":
                        if current < len(pages)-1:
                            current += 1
                        await msg.remove_reaction(u"\u27A1", ctx.author)

                    elif reaction.emoji == u"\u23E9":
                        current = len(pages)-1
                        await msg.remove_reaction(u"\u23E9", ctx.author)

                    if current != previous_page:
                        await msg.edit(embed=pages[current].set_footer(text=f"{current+1}/{len(pages)}"))
        except FileNotFoundError:
            embed=discord.Embed(title=f'{ops} Seraphine: Skins', description=f"No champion with that name was found!", color=0xfda5b0)
            await ctx.send(embed=embed)
        except Exception:
            traceback.print_exc()
              
    @skins.error
    async def skins_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(title=f'{ops} Seraphine: Skins', description="You need to give me a champion!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!skins [champion]`')
            await ctx.send(embed=embed) 
            
    @commands.command()
    async def matchup(self, ctx, champion, role=None):
        weak = '<:red_diamond:834133775877013525>'
        strong = '<:blue_diamond:834133776060907591>'
        roles = ['adc', 'top', 'mid', 'jungle', 'support']
        
        with open(f'dragontail/{version}/data/en_GB/championFull.json', encoding='utf-8') as f:
            champions = json.load(f)
        champions_data = champions['data']
        champion_key = None
        for k,v in champions_data.items():
            if champion.lower() == v['name'].lower() or champion.lower() == k.lower():
                champion = v['id']
                champion_key = v['key']
                champion_image = v['image']['full']
        f.close()
        
        
        if role is None:
            page = requests.get(f'https://app.mobalytics.gg/lol/champions/{champion}/build')
        elif role.lower() in roles:
            page = requests.get(f'https://app.mobalytics.gg/lol/champions/{champion}/build?role={role}')
        else:
            embed=discord.Embed(description="Invalid role!", color=0xfda5b0)
            embed.add_field(name='Roles', value='`top` `jungle` `mid` `adc` `support`')
            await ctx.send(embed=embed) 
            
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        
        weak_againt = []
        weak_againt_percentage = []
        strong_againt = []
        strong_againt_percentage = []
        best_synergy = []
        best_synergy_percentage = []

        if soup.find(class_='css-6q4pt9'):
            title = soup.find(class_='css-4hiyg0').text 
            default = soup.find('div', style=lambda value: value and 'border-color:var(--gold);' in value)
            default_role = default('img')[0]['alt']
                
            with open('data/roles.json') as f:
                rolesjson = json.load(f)
            role_icon = ''
            for r in rolesjson:
                if r['id'].lower() == default_role.lower():
                    role_icon = r['emoji']
                    
            for i in soup.find_all(class_='css-1ontmkt')[:3]:
                weak_againt.append(i.text)
            for i in soup.find_all(class_='css-yvp3r6')[:3]:
                weak_againt_percentage.append(i.text)    

            for i in soup.find_all(class_='css-1ontmkt')[3:6]:
                strong_againt.append(i.text)
            for i in soup.find_all(class_='css-gmg2a0')[:3]:
                strong_againt_percentage.append(i.text) 

            for i in soup.find_all(class_='css-1ontmkt')[6:9]:
                best_synergy.append(i.text)
            for i in soup.find_all(class_='css-gmg2a0')[3:6]:
                best_synergy_percentage.append(i.text)
                
                
            with open('data/championIcons.json', encoding='utf-8') as f:
                emojis = json.load(f)
            for e in emojis:
                if e['name'] == weak_againt[0]:
                    emoji_weak_uno = e['emoji']
                if e['name'] == weak_againt[1]:
                    emoji_weak_dos = e['emoji']
                if e['name'] == weak_againt[2]:
                    emoji_weak_tres = e['emoji']
                if e['name'] == strong_againt[0]:
                    emoji_strong_uno = e['emoji']
                if e['name'] == strong_againt[1]:
                    emoji_strong_dos = e['emoji']
                if e['name'] == strong_againt[2]:
                    emoji_strong_tres = e['emoji']
                if e['name'] == best_synergy[0]:
                    emoji_synergy_uno = e['emoji']
                if e['name'] == best_synergy[1]:
                    emoji_synergy_dos = e['emoji']
                if e['name'] == best_synergy[2]:
                    emoji_synergy_tres = e['emoji']
            f.close()
            
            try:
                embed = discord.Embed(description=f'Results for role: {role_icon} \n \u200B', color=0xfda5b0)
                embed.set_author(name=f'{title}', icon_url=f'https://seraphine-bot.s3.eu-central-1.amazonaws.com/champion/{champion_image}')
                embed.add_field(name=f'{weak} WEAK AGAINST', value=f'{emoji_weak_uno} **{weak_againt[0]}** \n {weak_againt_percentage[0]} \n Win Rate')
                embed.add_field(name='\u200B', value=f'{emoji_weak_dos} **{weak_againt[1]}** \n {weak_againt_percentage[1]} \n Win Rate')
                embed.add_field(name='\u200B', value=f'{emoji_weak_tres} **{weak_againt[2]}** \n {weak_againt_percentage[2]} \n Win Rate')
                embed.add_field(name='\u200B', value=f'\u200B', inline=False)
                embed.add_field(name=f'{strong} STRONG AGAINST', value=f'{emoji_strong_uno} **{strong_againt[0]}** \n {strong_againt_percentage[0]} \n Win Rate')
                embed.add_field(name='\u200B', value=f'{emoji_strong_dos} **{strong_againt[1]}** \n {strong_againt_percentage[1]} \n Win Rate')
                embed.add_field(name='\u200B', value=f'{emoji_strong_tres} **{strong_againt[2]}** \n {strong_againt_percentage[2]} \n Win Rate')
                embed.add_field(name='\u200B', value=f'\u200B', inline=False)
                embed.add_field(name=f'{strong} BEST SYNERGY', value=f'{emoji_synergy_uno} **{best_synergy[0]}** \n {best_synergy_percentage[0]} \n Win Rate')
                embed.add_field(name='\u200B', value=f'{emoji_synergy_dos} **{best_synergy[1]}** \n {best_synergy_percentage[1]} \n Win Rate')
                embed.add_field(name='\u200B', value=f'{emoji_synergy_tres} **{best_synergy[2]}** \n {best_synergy_percentage[2]} \n Win Rate')
                embed.set_image(url=f'https://raw.githubusercontent.com/buga-sys/championHeaders/master/{champion_key}.png')
                await ctx.send(embed=embed)
            except:
                traceback.print_exc()
                embed=discord.Embed(title=f'{ops} Seraphine: Matchup', description=f"Something went wrong! Couldn't get data.", color=0xfda5b0)
                await ctx.send(embed=embed)
        else:
            if role is None:
                embed=discord.Embed(title=f'{ops} Seraphine: Matchup', description=f"No data was found! \n \u200B \n Champion: **{champion.capitalize()}**", color=0xfda5b0)
                await ctx.send(embed=embed) 
            else:
                embed=discord.Embed(title=f'{ops} Seraphine: Matchup', description=f"No data was found! \n \u200B \n Champion: **{champion.capitalize()}** \n Role: **{role.capitalize()}**", color=0xfda5b0)
                await ctx.send(embed=embed) 
        
    @matchup.error
    async def matchup_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(title=f'{ops} Seraphine: Matchup', description="You need to give me a champion!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!matchup [champion] [optional: role]`')
            await ctx.send(embed=embed) 

    @commands.command(aliases=['counters'])
    async def counter(self, ctx, champion, role=None):
        weak = '<:red_diamond:834133775877013525>'
        strong = '<:blue_diamond:834133776060907591>'
        roles = ['adc', 'top', 'mid', 'jungle', 'support']
        
        with open(f'dragontail/{version}/data/en_GB/championFull.json', encoding='utf-8') as f:
            champions = json.load(f)
        champions_data = champions['data']
        champion_key = None
        for k,v in champions_data.items():
            if champion.lower() == v['name'].lower() or champion.lower() == k.lower():
                champion = v['id']
                champion_key = v['key']
                champion_image = v['image']['full']
        f.close()
        
        if role is None:
            page = requests.get(f'https://app.mobalytics.gg/lol/champions/{champion}/counters')
        elif role.lower() in roles:
            page = requests.get(f'https://app.mobalytics.gg/lol/champions/{champion}/counters?role={role}')
        else:
            embed=discord.Embed(description="Invalid role!", color=0xfda5b0)
            embed.add_field(name='Roles', value='`top` `jungle` `mid` `adc` `support`')
            await ctx.send(embed=embed) 
            
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        if soup.find(class_='css-x4zg72'):
            title = soup.find(class_='css-122656p').text
            default = soup.find('div', style=lambda value: value and 'border-color:var(--gold);' in value)
            default_role = default('img')[0]['alt']
                
            with open('data/roles.json') as f:
                rolesjson = json.load(f)
            role_icon = ''
            for r in rolesjson:
                if r['id'].lower() == default_role.lower():
                    role_icon = r['emoji']
                    
            table = soup.find_all(class_='css-19id55f')
            counters = []
            blank = '<:BLANK:837828544410550282>'

            for c in table[:12]:
                champion = c.find(class_='css-4fiab5').text
                matches = c.find(class_='css-9zgxyq').text
                win_rate = c.find_all(class_='css-a632yi')[1].text
                counter = [champion, matches, win_rate]
                counters.append(counter)
            counters.sort(key= lambda x: float(x[2][:-1]), reverse=True)
            nl = '\n'
            
            for c in counters:
                newstring = blank + c[2]
                c[2] = newstring
            
            for c in counters:
                newstring = c[1] + blank
                c[1] = newstring    

            with open('data/championIcons.json', encoding='utf-8') as f:
                emojis = json.load(f)
            for e in emojis:
                for c in counters:
                    if e['name'] == c[0]:
                        emoji = e['emoji']
                        newstring = emoji + ' ' + c[0]
                        c[0] = newstring
            f.close()
            
            try:
                embed = discord.Embed(description=f'Results for role: {role_icon} \n \u200B', color=0xfda5b0)
                embed.set_author(name=f'{title}', icon_url=f'https://seraphine-bot.s3.eu-central-1.amazonaws.com/champion/{champion_image}')
                embed.add_field(name='Champions', value=f"**{f'{nl}'.join([c[0] for c in counters])}**")
                embed.add_field(name='Matches', value=f"{f'{nl}'.join([c[1] for c in counters])}")
                embed.add_field(name=f'{blank}Win Rate', value=f"{f'{nl}'.join([c[2] for c in counters])}")
                embed.set_image(url=f'https://raw.githubusercontent.com/buga-sys/championHeaders/master/{champion_key}.png')
                await ctx.send(embed=embed)
            except:
                traceback.print_exc()
                embed=discord.Embed(title=f'{ops} Seraphine: Counters', description=f"Something went wrong! Couldn't get data.", color=0xfda5b0)
                await ctx.send(embed=embed)
        else:
            if role is None:
                embed=discord.Embed(title=f'{ops} Seraphine: Counters', description=f"No data was found! \n \u200B \n Champion: **{champion.capitalize()}**", color=0xfda5b0)
                await ctx.send(embed=embed) 
            else:
                embed=discord.Embed(title=f'{ops} Seraphine: Counters', description=f"No data was found! \n \u200B \n Champion: **{champion.capitalize()}** \n Role: **{role.capitalize()}**", color=0xfda5b0)
                await ctx.send(embed=embed) 
                
    @counter.error
    async def counter_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(title=f'{ops} Seraphine: Counters', description="You need to give me a champion!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!counters [champion] [optional: role]`')
            await ctx.send(embed=embed)  
    
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
    
    @commands.command(aliases=['championrates'])
    async def championrate(self, ctx, *, champion):
        with open('lolstaticdata/rates.json', encoding='utf-8') as f:
            rates = json.load(f)

        with open('data/championIcons.json', encoding='utf-8') as w:
            emojis = json.load(w)
            
        playRate = None
        winRate = None
        banRate = None

        for e in emojis:
            for k,v in rates['data'].items():
                for q,w in v.items():
                    if k == e['key']:
                        name = e['name']
                        cid = e['id']
                        if champion.lower() == name.lower() or champion.lower() == cid.lower():
                            champion_id = e['id']
                            champion_key = e['key']
                            playRate = w['playRate']
                            winRate = w['winRate']
                            banRate = w['banRate']
        
        embed = discord.Embed(description='Champion game stats: \n \u200B',color=0xfda5b0)
        embed.set_author(name=f'{champion.capitalize()} Rates', icon_url=f'https://seraphine-bot.s3.eu-central-1.amazonaws.com/champion/{champion_id}.png')
        embed.add_field(name='Play Rate', value=f'{playRate}%')
        embed.add_field(name='Win Rate', value=f'{winRate}%')
        embed.add_field(name='Ban Rate', value=f'{banRate}%')
        embed.set_image(url=f'https://raw.githubusercontent.com/buga-sys/championHeaders/master/{champion_key}.png')
        await ctx.send(embed=embed)
        
    @commands.command()
    async def build(self, ctx, champion, role=None):
        roles = ['adc', 'top', 'mid', 'jungle', 'support']
        
        with open(f'dragontail/{version}/data/en_GB/championFull.json', encoding='utf-8') as f:
            champions = json.load(f)
        champions_data = champions['data']
        champion_key = None
        for k,v in champions_data.items():
            if champion.lower() == v['name'].lower() or champion.lower() == k.lower():
                champion = v['id']
                champion_key = v['key']
                champion_image = v['image']['full']
        f.close()
        
        if role is None:
            page = requests.get(f'https://app.mobalytics.gg/lol/champions/{champion}/build')
        elif role.lower() in roles:
            page = requests.get(f'https://app.mobalytics.gg/lol/champions/{champion}/build?role={role}')
        else:
            embed=discord.Embed(description="Invalid role!", color=0xfda5b0)
            embed.add_field(name='Roles', value='`top` `jungle` `mid` `adc` `support`')
            await ctx.send(embed=embed) 
            
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        if soup.find(class_='css-2ps0tg'):
            #Role
            default = soup.find('div', style=lambda value: value and 'border-color:var(--gold);' in value)
            default_role = default('img')[0]['alt']
                
            with open('data/roles.json') as f:
                rolesjson = json.load(f)
            role_icon = ''
            for r in rolesjson:
                if r['id'].lower() == default_role.lower():
                    role_icon = r['emoji']
                    
            #Runes
            mainPath = soup.find_all(class_='css-18ujv6b')[0]['alt']
            keyStone = soup.find(class_='css-1bdyqpk')['alt']
            mainSlotOne = soup.find_all(class_='css-1054us4')[0]['alt']
            mainSlotTwo = soup.find_all(class_='css-1054us4')[1]['alt']
            mainSlotThree = soup.find_all(class_='css-1054us4')[2]['alt']
            secPath = soup.find_all(class_='css-18ujv6b')[1]['alt']
            secSlotOne = soup.find_all(class_='css-1054us4')[3]['alt']
            secSlotTwo = soup.find_all(class_='css-1054us4')[4]['alt']
            
            with open(f'data/runeIcons.json', encoding='utf-8') as f:
                runes = json.load(f)
            
            for r in runes:
                if r['name'] == mainPath:
                    mainPath = r['emoji'] + ' ' + r['name']
                if r['name'] == keyStone:
                    keyStone = r['emoji']
                if r['name'] == mainSlotOne:
                    mainSlotOne = r['emoji']
                if r['name'] == mainSlotTwo:
                    mainSlotTwo = r['emoji']
                if r['name'] == mainSlotThree:
                    mainSlotThree = r['emoji']
                if r['name'] == secPath:
                    secPath = r['emoji'] + ' ' + r['name']
                if r['name'] == secSlotOne:
                    secSlotOne = r['emoji']
                if r['name'] == secSlotTwo:
                    secSlotTwo = r['emoji']
            f.close()     

            #Shards
            shardOne = soup.find_all(class_='css-1vgqbrs')[0]['src']
            shardTwo = soup.find_all(class_='css-1vgqbrs')[1]['src']
            shardThree = soup.find_all(class_='css-1vgqbrs')[2]['src']
            
            with open(f'data/shards.json', encoding='utf-8') as f:
                shards = json.load(f)
            
            for s in shards:
                if s['id'] in shardOne:
                    shardOne = s['emoji']
                if s['id'] in shardTwo:
                    shardTwo = s['emoji']
                if s['id'] in shardThree:
                    shardThree = s['emoji']
            
            #Summoners
            summonerNames = []
            with open(f'dragontail/11.9.1/data/en_GB/summoner.json', encoding='utf-8') as f:
                summoner = json.load(f)
            for s in summoner['data']:
                for df in soup.find_all(class_='css-erhaoi'):
                    if s in df['src']:
                        summonerNames.append(s)
            f.close()

            with open(f'data/summonerIcons.json', encoding='utf-8') as f:
                summonerIcons = json.load(f)

            summonerEmojis = []
            for i in summonerIcons:
                for n in summonerNames:
                    if i['id'] == n:
                        summonerEmojis.append(i['emoji'])
            f.close()
                    
            #Skills
            skillEmojis = [
                    {
                    "name": "Q",
                    "emoji": "<:q:841775869856710688>"
                    },
                    {
                    "name": "W",
                    "emoji": "<:w:841775870100242512>"
                    },
                    {
                    "name": "E",
                    "emoji": "<:e:841775869852385332>"
                    },
                    {
                    "name": "R",
                    "emoji": "<:r:841775870158569512>"
                    }
                ]

            skills = []
            for i in soup.find_all(class_='css-hgy7ai etewe3q4'):
                for s in skillEmojis:
                    if i.text == s['name']:
                        skills.append(s['emoji'])
            
            #Items
            starterItems = [i['src'] for i in soup.find_all(class_='css-8atqhb')[0].find_all('img')]
            earlyItems = [i['src'] for i in soup.find_all(class_='css-8atqhb')[1].find_all('img')]
            coreItems = [i['src'] for i in soup.find_all(class_='css-8atqhb')[2].find_all('img')]
            fullItems = [i['src'] for i in soup.find_all(class_='css-8atqhb')[3].find_all('img')]
            situationalItems = [i['src'] for i in soup.find(class_='css-ahi832').find_all('img')]
            starterEmojis = []
            earlyEmojis = []
            coreEmojis = []
            fullEmojis = []
            situationalEmojis = []
            
            with open(f'data/itemIcons.json', encoding='utf-8') as f:
                items = json.load(f)
                
            for i in items:
                for s in starterItems:
                    if i['id'] in s:
                        starterEmojis.append(i['emoji'])
                for s in earlyItems:
                    if i['id'] in s:
                        earlyEmojis.append(i['emoji'])
                for s in coreItems:
                    if i['id'] in s:
                        coreEmojis.append(i['emoji'])
                for s in fullItems:
                    if i['id'] in s:
                        fullEmojis.append(i['emoji'])
                for s in situationalItems:
                    if i['id'] in s:
                        situationalEmojis.append(i['emoji'])
            
            try:
                embed = discord.Embed(description=f'Results for role: {role_icon} \n \u200B', color=0xfda5b0)
                embed.set_author(name=f'{champion.capitalize()} · Most Popular Build', icon_url=f'https://seraphine-bot.s3.eu-central-1.amazonaws.com/champion/{champion_image}')
                embed.set_image(url=f'https://raw.githubusercontent.com/buga-sys/championHeaders/master/{champion_key}.png')
                embed.add_field(name=f"Runes", value=f"**{mainPath}** \n {keyStone} \n {mainSlotOne} \n {mainSlotTwo} \n {mainSlotThree}")
                embed.add_field(name=f"\u200B", value=f"""**{secPath}** \n {secSlotOne} \n {secSlotTwo}
                                \u200B
                                {shardOne}
                                {shardTwo}
                                {shardThree}
                                """)
                embed.add_field(name=f"Items", value=f"""
                                Starter
                                {' '.join([i for i in starterEmojis])}
                                \u200B
                                Early Items
                                {' '.join([i for i in earlyEmojis])}
                                \u200B
                                Core Items
                                {' '.join([i for i in coreEmojis])}
                                \u200B
                                Full Build
                                {' '.join([i for i in fullEmojis])}
                                \u200B
                                """)
                embed.add_field(name='Spells', value=f"{' '.join([s for s in summonerEmojis])} \n \u200B")
                embed.add_field(name='\u200B', value=f"\u200B")
                embed.add_field(name='Situational Items', value=f"{' '.join([i for i in situationalEmojis])}")
                embed.add_field(name='Skill Order', value=f"{'>'.join([s for s in skills])}", inline=False)
                await ctx.send(embed=embed)
            except:
                traceback.print_exc()
                embed=discord.Embed(title=f'{ops} Seraphine: Build', description=f"Something went wrong! Couldn't get data.", color=0xfda5b0)
                await ctx.send(embed=embed)         
            
        else:
            if role is None:
                embed=discord.Embed(title=f'{ops} Seraphine: Build', description=f"No data was found! \n \u200B \n Champion: **{champion.capitalize()}**", color=0xfda5b0)
                await ctx.send(embed=embed) 
            else:
                embed=discord.Embed(title=f'{ops} Seraphine: Build', description=f"No data was found! \n \u200B \n Champion: **{champion.capitalize()}** \n Role: **{role.capitalize()}**", color=0xfda5b0)
                await ctx.send(embed=embed) 
    
    @build.error
    async def build_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(title=f'{ops} Seraphine: Build', description="You need to give me a champion!", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!build [champion] [optional: role]`')
            await ctx.send(embed=embed) 

def setup(client):
    client.add_cog(Champions(client))