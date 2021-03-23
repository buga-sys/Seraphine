import discord
from discord.ext import commands
import json
import re

version = '11.6.1'

class Items(commands.Cog):
    def __init__(self, client):
        self.client = client   
   
    @commands.command(aliases=['i'])
    async def item(self, ctx, *, value):
        try:
            with open(f'dragontail\\{version}\\data\\en_GB\\item.json', encoding='utf-8') as f:
                items = json.load(f)
            
            item = value
            name = None
            description = None
            plaintext = None
            tags = []
            item_png = None

            for k,v in items['data'].items():
                if v['name'].lower() == item.lower():
                    name = v['name']
                    description = v['description']
                    plaintext = v['plaintext']
                    tags = v['tags']
                    item_png = v['image']['full']
            f.close()
            
            item_image_path = f'dragontail\\{version}\\img\\item\\'
            image_full_path = item_image_path + item_png
            # clean = re.compile('<.*?>')
            # description_clean = re.sub(clean, '\n', description)
            # description_clean = re.sub(r'\n\s*\n', '\n\n', description_clean)
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
            description = description.replace('<scaleAD>', '*')
            description = description.replace('</scaleAD>', '*')
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
            
            file = discord.File(f"{image_full_path}", filename=f"{item_png}")
            embed = discord.Embed(title=f'{name}', description=f'{plaintext}')
            embed.set_thumbnail(url=f'attachment://{item_png}')
            embed.set_footer(text=f"{', '.join(tags)}")
            embed.add_field(name='\u200B', value=f'{description}')
            await ctx.send(file=file, embed=embed)
        except Exception as e:
            print(e)
        

def setup(client):
    client.add_cog(Items(client))