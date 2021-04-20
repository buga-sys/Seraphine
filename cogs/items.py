import discord
from discord.ext import commands
import json
import re
import asyncio
import traceback
import os
from dotenv import load_dotenv

load_dotenv()
version = str(os.getenv('VERSION'))

class Items(commands.Cog):
    def __init__(self, client):
        self.client = client   
   
    @commands.command()
    async def item(self, ctx, *, value):
        try:
            with open(f'dragontail/{version}/data/en_GB/item.json', encoding='utf-8') as f:
                items = json.load(f)
            
            item = value
            name = None
            description = None
            plaintext = None
            tags = []
            item_png = None
            gold_total = None

            for k,v in items['data'].items():
                if item.lower() in v['name'].lower():
                    name = v['name']
                    description = v['description']
                    plaintext = v['plaintext']
                    tags = v['tags']
                    item_png = v['image']['full']
                    gold_total = v['gold']['total']
            f.close()
            
            item_image_path = f'dragontail/{version}/img/item/'
            image_full_path = item_image_path + item_png
            description = description.replace('<mainText>', '')
            description = description.replace('</mainText>', '')
            description = description.replace('<stats>', '```ml\n\u200B\n')
            description = description.replace('</stats>', '\n\u200B```')
            description = description.replace('<attention>', '')
            description = description.replace('</attention>', '')
            description = description.replace('<passive>', '**')
            description = description.replace('</passive>', '**')
            description = description.replace('<li>', '')
            description = description.replace('</li>', '')
            description = description.replace('<status>', '__')
            description = description.replace('</status>', '__')
            description = description.replace('<rules>', '')
            description = description.replace('</rules>', '')
            description = description.replace('<active>', '**')
            description = description.replace('</active>', '**')
            description = description.replace('<magicDamage>', '*')
            description = description.replace('</magicDamage>', '*')
            description = description.replace('<physicalDamage>', '*')
            description = description.replace('</physicalDamage>', '*')
            description = description.replace('<scaleAP>', '*')
            description = description.replace('</scaleAP>', '*')
            description = description.replace('<attackSpeed>', '*')
            description = description.replace('</attackSpeed>', '*')
            description = description.replace('<scaleAD>', '*')
            description = description.replace('</scaleAD>', '*')
            description = description.replace('<OnHit>', '*')
            description = description.replace('</OnHit>', '*')
            description = description.replace('<scaleMana>', '*')
            description = description.replace('</scaleMana>', '*')
            description = description.replace('<scaleLevel>', '*')
            description = description.replace('</scaleLevel>', '*')
            description = description.replace('<scaleHealth>', '*')
            description = description.replace('</scaleHealth>', '*')
            description = description.replace('<speed>', '*')
            description = description.replace('</speed>', '*')
            description = description.replace('<trueDamage>', '*')
            description = description.replace('</trueDamage>', '*')
            description = description.replace('<lifeSteal>', '*')
            description = description.replace('</lifeSteal>', '*')
            description = description.replace('<keywordStealth>', '*')
            description = description.replace('</keywordStealth>', '*')
            description = description.replace('<rarityMythic>', '**')
            description = description.replace('</rarityMythic>', '**')
            description = description.replace('<rarityLegendary>', '**')
            description = description.replace('</rarityLegendary>', '**')
            description = description.replace('<br>', '\n')
            rx = r"\.(?=\S)"
            description = re.sub(rx, ". ", description)
            
            file = discord.File(f"{image_full_path}", filename=f"{item_png}")
            embed = discord.Embed(title=f'{name}', description=f'<:gold:823209384942370836>{gold_total}', color=0xfda5b0)
            embed.set_thumbnail(url=f'attachment://{item_png}')
            embed.add_field(name='\u200B', value=f'{description}')
            await ctx.send(file=file, embed=embed)
        except IndexError:
            await ctx.send("That's not a valid item name.")
        except TypeError:
            await ctx.send("That's not a valid item name.")
        except Exception:
            traceback.print_exc()
    
    @item.error
    async def item_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(description="Display information about an item.", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!item [item]`')
            embed.add_field(name='Example', value='`!item infinity edge`')
            await ctx.send(embed=embed) 
            
    @commands.command()
    async def itemtype(self, ctx, *, value):
        try:
            with open(f'dragontail/{version}/data/en_GB/item.json', encoding='utf-8') as f:
                items = json.load(f)
            
            itemtype = value
            name = None
            description = None
            plaintext = None
            tags = []
            item_png = None
            pages = []
            files = []
            buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
            current = 0
            item_image_path = f'dragontail/{version}/img/item/'
            gold_total = None
            
            def find_between( s, first, last ):
                        try:
                            start = s.index( first ) + len( first )
                            end = s.index( last, start )
                            return s[start:end]
                        except ValueError:
                            return ""   

            for k,v in items['data'].items():
                if itemtype.lower() in find_between(str(v['description']).lower(), '<stats>', '</stats>'):
                    name = v['name']
                    description = v['description']
                    description = description.replace('<mainText>', '')
                    description = description.replace('</mainText>', '')
                    description = description.replace('<stats>', '```ml\n\u200B\n')
                    description = description.replace('</stats>', '\n\u200B```')
                    description = description.replace('<attention>', '')
                    description = description.replace('</attention>', '')
                    description = description.replace('<passive>', '**')
                    description = description.replace('</passive>', '**')
                    description = description.replace('<li>', '')
                    description = description.replace('</li>', '')
                    description = description.replace('<status>', '__')
                    description = description.replace('</status>', '__')
                    description = description.replace('<rules>', '')
                    description = description.replace('</rules>', '')
                    description = description.replace('<active>', '**')
                    description = description.replace('</active>', '**')
                    description = description.replace('<magicDamage>', '*')
                    description = description.replace('</magicDamage>', '*')
                    description = description.replace('<physicalDamage>', '*')
                    description = description.replace('</physicalDamage>', '*')
                    description = description.replace('<OnHit>', '*')
                    description = description.replace('</OnHit>', '*')
                    description = description.replace('<scaleAP>', '*')
                    description = description.replace('</scaleAP>', '*')
                    description = description.replace('<scaleAD>', '*')
                    description = description.replace('</scaleAD>', '*')
                    description = description.replace('<attackSpeed>', '*')
                    description = description.replace('</attackSpeed>', '*')
                    description = description.replace('<scaleMana>', '*')
                    description = description.replace('</scaleMana>', '*')
                    description = description.replace('<scaleLevel>', '*')
                    description = description.replace('</scaleLevel>', '*')
                    description = description.replace('<scaleHealth>', '*')
                    description = description.replace('</scaleHealth>', '*')
                    description = description.replace('<healing>', '*')
                    description = description.replace('</healing>', '*')
                    description = description.replace('<speed>', '*')
                    description = description.replace('</speed>', '*')
                    description = description.replace('<trueDamage>', '*')
                    description = description.replace('</trueDamage>', '*')
                    description = description.replace('<lifeSteal>', '*')
                    description = description.replace('</lifeSteal>', '*')
                    description = description.replace('<keywordStealth>', '*')
                    description = description.replace('</keywordStealth>', '*')
                    description = description.replace('<rarityMythic>', '**')
                    description = description.replace('</rarityMythic>', '**')
                    description = description.replace('<rarityLegendary>', '**')
                    description = description.replace('</rarityLegendary>', '**')
                    description = description.replace('<br>', '\n')
                    rx = r"\.(?=\S)"
                    description = re.sub(rx, ". ", description)
                    plaintext = v['plaintext']
                    tags = v['tags']
                    item_png = v['image']['full']
                    gold_total = v['gold']['total']
                    image_full_path = item_image_path + item_png
                    # file = discord.File(f"{image_full_path}", filename=f"{item_png}")
                    # files.append(file)
                    page = discord.Embed(title=f'{name}', description=f'<:gold:823209384942370836>{gold_total}', color=0xfda5b0).set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/{version}/img/item/{item_png}').add_field(name='\u200B', value=f'{description}')
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
            await ctx.send("That's not a valid item type.")
        except TypeError:
            await ctx.send("That's not a valid item type.")
        except Exception:
            traceback.print_exc()

    @itemtype.error
    async def itemtype_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(description="Display items of specific type.", color=0xfda5b0)
            embed.add_field(name='Usage', value='`!itemtype [type]`')
            embed.add_field(name='Example', value='`!itemtype ability power`')
            await ctx.send(embed=embed)      

def setup(client):
    client.add_cog(Items(client))