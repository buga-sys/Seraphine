import discord
from discord.ext import commands
import json

api = 'RGAPI-6a15b991-08e8-4373-bcde-83594bdc51a6'
version = '11.6.1'

class Champions(commands.Cog):
    def __init__(self, client):
        self.client = client   
   
    @commands.command(aliases=['c'])
    async def champion(self, ctx, value):
        with open(f'dragontail\\{version}\\data\\en_GB\\championFull.json', encoding='utf-8') as f:
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
        images_path = f'dragontail\\{version}\\img\\champion\\'
        champion_image = None
        passive_name = None
        passive_description = None

        for k,v in champions_data.items():
            if k.lower() == champion:
                name = v['name']
                title = v['title']
                champion_image = v['image']['full']
                partype = v['partype']
                for tag in v['tags']:
                    tags.append(tag)
                for spell in v['spells']:
                    spells_names.append(spell['name'])  
                    spells_description.append(spell['description'])
                    spells_cd.append(spell['cooldown'])
                passive_name = v['passive']['name']
                passive_description = v['passive']['description']
        image_full_path = images_path + champion_image
        f.close()
        
        file = discord.File(f"{image_full_path}", filename=f"{champion_image}")
        embed = discord.Embed(title=f'{name} - {title}', description=f'''{', '.join(tags)} \n Partype: {partype}''')
        embed.set_thumbnail(url=f'attachment://{champion_image}')
        embed.add_field(name=f'(Passive) {passive_name}', value=f"{passive_description}", inline=False)
        embed.add_field(name=f'(Q) {spells_names[0]}', value=f"{'/'.join(map(str, spells_cd[0]))} \n {spells_description[0]})", inline=False)
        embed.add_field(name=f'(W) {spells_names[1]}', value=f"{'/'.join(map(str, spells_cd[1]))} \n {spells_description[1]}", inline=False)
        embed.add_field(name=f'(E) {spells_names[2]}', value=f"{'/'.join(map(str, spells_cd[2]))} \n {spells_description[2]}", inline=False)
        embed.add_field(name=f'(R) {spells_names[3]}', value=f"{'/'.join(map(str, spells_cd[3]))} \n {spells_description[3]}", inline=False)
        await ctx.send(file=file, embed=embed)

def setup(client):
    client.add_cog(Champions(client))