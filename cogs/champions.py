import discord
from discord.ext import commands
import json
import re
import traceback
import asyncio

version = '11.7.1'

class Champions(commands.Cog):
    def __init__(self, client):
        self.client = client   
   
    @commands.command()
    async def champion(self, ctx, value):
        if len(value) > 2:
            try:
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
                spells_cd = []
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
                            tags.append(tag)
                        for spell in v['spells']:
                            spells_names.append(spell['name'])
                            clean = re.compile('<.*?>')
                            description = re.sub(clean, "", spell['description'])  
                            spells_description.append(description)
                            spells_cd.append(spell['cooldown'])
                        passive_name = v['passive']['name']
                        passive_description = v['passive']['description']
                        clean = re.compile('<.*?>')
                        passive_description = re.sub(clean, "", passive_description)
                image_full_path = images_path + champion_image
                f.close()
                
                file = discord.File(f"{image_full_path}", filename=f"{champion_image}")
                embed = discord.Embed(title=f'{name} - {title.title()}', description=f'''{', '.join(tags)} \n Partype: {partype}''', color=0xfda5b0)
                embed.set_thumbnail(url=f'attachment://{champion_image}')
                embed.add_field(name=f'(Passive) {passive_name}', value=f"{passive_description}", inline=False)
                embed.add_field(name=f'(Q) {spells_names[0]}', value=f"{'/'.join(map(str, spells_cd[0]))} \n {spells_description[0]}", inline=False)
                embed.add_field(name=f'(W) {spells_names[1]}', value=f"{'/'.join(map(str, spells_cd[1]))} \n {spells_description[1]}", inline=False)
                embed.add_field(name=f'(E) {spells_names[2]}', value=f"{'/'.join(map(str, spells_cd[2]))} \n {spells_description[2]}", inline=False)
                embed.add_field(name=f'(R) {spells_names[3]}', value=f"{'/'.join(map(str, spells_cd[3]))} \n {spells_description[3]}", inline=False)
                await ctx.send(file=file, embed=embed)
            except TypeError:
                await ctx.send("That's not a valid champion name.")
            except Exception:
                traceback.print_exc()
        else:
            await ctx.send("That's not a valid champion name.")
    
    @champion.error
    async def champion_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(description="Display information about a champion\nUsage: `!champion [champion]` for example, `!champion annie`", color=0xfda5b0)
            await ctx.send(embed=embed) 
            
    @commands.command()
    async def skins(self, ctx, value):
        if len(value) > 2:
            try:

                champion = value.lower()
                with open(f'dragontail/{version}/data/en_GB/championFull.json', encoding='utf-8') as f:
                    champions = json.load(f)

                champions_data = champions['data']
                name = None
                images_path = f'dragontail/img/champion/loading/'
                skin_name = ''
                skin_id = ''
                pages = []
                buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
                current = 0

                for k,v in champions_data.items():
                    if champion.lower() in k.lower():
                        name = v['id']
                        for sid in v['skins']:
                            skin_name= sid['name']
                            skin_id = str(sid['num'])
                            skin_image = name + '_' + skin_id + '.jpg' 
                            # image_full_path = images_path + skin_image
                            page = discord.Embed(title=f'{skin_name}', color=0xfda5b0).set_image(url=f'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{skin_image}')
                            pages.append(page)    
                f.close()
                
                msg = await ctx.send(embed=pages[current].set_footer(text=f"{current+1}/{len(pages)}"))
                
                for button in buttons:
                    await msg.add_reaction(button)
                    
                while True:
                    try:
                        reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

                    except asyncio.TimeoutError:
                        pass

                    else:
                        previous_page = current
                        if reaction.emoji == u"\u23EA":
                            current = 0
                            
                        elif reaction.emoji == u"\u2B05":
                            if current > 0:
                                current -= 1
                                
                        elif reaction.emoji == u"\u27A1":
                            if current < len(pages)-1:
                                current += 1

                        elif reaction.emoji == u"\u23E9":
                            current = len(pages)-1

                        for button in buttons:
                            await msg.remove_reaction(button, ctx.author)

                        if current != previous_page:
                            await msg.edit(embed=pages[current].set_footer(text=f"{current+1}/{len(pages)}"))
            except IndexError:
                await ctx.send("That's not a valid champion name.")
                
            except Exception:
                traceback.print_exc()
        else:
            await ctx.send("That's not a valid champion name.")
        
            

def setup(client):
    client.add_cog(Champions(client))