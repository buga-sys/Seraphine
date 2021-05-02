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
                    if champion in k.lower():
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
            with open(f'lolstaticdata/champions/{champion.capitalize()}.json', encoding='utf-8') as f:
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
            cid = champions['name']
            picid = champions['key']
            
            for c in champions['skins'][1:]:
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
                page = discord.Embed(title='Seraphine: Skins', description="Here's what you asked for: \n \u200B", color=0xfda5b0).add_field(name=f'{rarity} {name}',value=f'{cost}').set_image(url=imageurl).set_author(name=f'{cid}', icon_url=f'https://seraphine-bot.s3.eu-central-1.amazonaws.com/champion/{picid}.png')
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
            if champion.lower() in k.lower():
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
            title = soup.find(class_='css-4hiyg0 e1c5gntn0').text
            default = soup.find('div', style=lambda value: value and 'border-color:var(--gold);' in value)
            default_role = default('img')[0]['alt']
                
            with open('data/roles.json') as f:
                rolesjson = json.load(f)
            role_icon = ''
            for r in rolesjson:
                if r['id'].lower() == default_role.lower():
                    role_icon = r['emoji']
                    
            for i in soup.find_all(class_='css-1w0si3o ebg788s4')[:3]:
                weak_againt.append(i.text)
            for i in soup.find_all(class_='css-1t0zj6v ebg788s6')[:3]:
                weak_againt_percentage.append(i.text)    

            for i in soup.find_all(class_='css-1w0si3o ebg788s4')[3:6]:
                strong_againt.append(i.text)
            for i in soup.find_all(class_='css-1t0zj6v ebg788s6')[3:6]:
                strong_againt_percentage.append(i.text) 

            for i in soup.find_all(class_='css-1w0si3o ebg788s4')[6:9]:
                best_synergy.append(i.text)
            for i in soup.find_all(class_='css-1t0zj6v ebg788s6')[6:9]:
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
            
            embed = discord.Embed(description=f'Results for role: {role_icon}', color=0xfda5b0)
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
            if champion.lower() in k.lower():
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
            title = soup.find(class_='css-122656p e1xyd8bn3').text
            default = soup.find('div', style=lambda value: value and 'border-color:var(--gold);' in value)
            default_role = default('img')[0]['alt']
                
            with open('data/roles.json') as f:
                rolesjson = json.load(f)
            role_icon = ''
            for r in rolesjson:
                if r['id'].lower() == default_role.lower():
                    role_icon = r['emoji']
                    
            table = soup.find_all(class_='css-16pn635 e1yssf620')
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
                embed = discord.Embed(description=f'Results for role: {role_icon}', color=0xfda5b0)
                embed.set_author(name=f'{title}', icon_url=f'https://seraphine-bot.s3.eu-central-1.amazonaws.com/champion/{champion_image}')
                embed.add_field(name='Champions', value=f"**{f'{nl}'.join([c[0] for c in counters])}**")
                embed.add_field(name='Matches', value=f"{f'{nl}'.join([c[1] for c in counters])}")
                embed.add_field(name=f'{blank}Win Rate', value=f"{f'{nl}'.join([c[2] for c in counters])}")
                
                embed.set_image(url=f'https://raw.githubusercontent.com/buga-sys/championHeaders/master/{champion_key}.png')
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title=f'{ops} Seraphine: Counters', description=f"No data was found! \n \u200B \n Champion: **{champion.capitalize()}** \n Role: **{role.capitalize()}**", color=0xfda5b0)
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

def setup(client):
    client.add_cog(Champions(client))