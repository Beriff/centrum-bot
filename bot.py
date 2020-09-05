import discord
import requests
import re
from bs4 import BeautifulSoup

from discord.utils import get
from discord.ext import commands

userTable = {}
superiumShop = "https://superium.net/Shop/"
assetLink = "https://superium.net/assets/thumbnails/catalog/"
userLink = "https://superium.net/user/"
gameLink = "https://superium.net/games/"

client = commands.Bot(command_prefix='sc!')



@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('sc!help'))
    print('[SC] Bot Ready')

@client.command()
async def assign(ctx, id):

    id = int(id)
    userTable[ctx.author.name] = id

    page = requests.get(userLink + str(id)).text
    soup = BeautifulSoup(page, "lxml")
    replace = '<h1 class="title is-3">'
    name = str(soup.find('h1', class_="title is-3")).replace(replace, '').replace("</h1>", "")

    await ctx.send(f'account assigned to {name}')



@client.command()
async def asset(ctx, id):
    global superiumShop
    global assetLink
    global assetChannel
    global tradeChannel
    assetChannel = client.get_channel(750314833101979661)
    tradeChannel = client.get_channel(750314777460473957)

    try:
        if type(userTable[ctx.author.name]) is int:

            stud = discord.utils.get(client.emojis, name='stud')
            brick = discord.utils.get(client.emojis, name='brick')

            assetLink = assetLink + id + ".png"
            superiumShop = superiumShop + id
            page = requests.get(superiumShop).text
            soup = BeautifulSoup(page, "lxml")
            name = soup.find('h1', class_="title is-4")
            name = str(name).replace('<h1 class="title is-4">', '')
            name = name.replace('</h1>', '')

            description = soup.find('blockquote')
            description = str(description).replace("<blockquote>", '')
            description = description.replace("</blockquote>", '')

            price = soup.find('span', {"style":"font-size: 20px;"})

            item = soup.find('h1', class_="subtitle is-6")

            author = re.sub(r'<a href="\/user\/[0-9]{1,5}">', '', str(item).replace('Superium', '').replace('by', '').replace('Shirt', '').replace('Pants', '').replace('<h1 class="subtitle is-6">', '').replace('</a></h1>', ''))

            if "Shirt" in str(item):
                item = "Shirt"
            elif "Pants" in str(item):
                item = "Pants"
            else:
                item = False
            if item:
                embed = discord.Embed(description=f"{description}", title=f"{item} Announcement! {name}",  colour=discord.Color.red())
                embed.set_thumbnail(url=assetLink)
                embed.add_field(name="Author", value=f"{author}")
                embed.add_field(name="Sent by", value=f'{ctx.author.name}')
                replace = '<span style="font-size: 20px;">'

                priceType = soup.find('img', {"width":"16"})
                isBrick = False
                if "brick" in str(priceType):
                    isBrick = True

                if isBrick:
                    embed.add_field(name="Price", value=f'{brick} {str(price).replace(replace, "").replace("</span>", "") }')
                else:
                    embed.add_field(name="Price", value=f'{stud} {str(price).replace(replace, "").replace("</span>", "") }')

                await assetChannel.send(embed=embed)
            else:
                await ctx.send('Missing permission to claim hat/tool!')

            superiumShop = "https://superium.net/Shop/"
            assetLink = "https://superium.net/assets/thumbnails/catalog/"
    except KeyError:
        await ctx.send('assign your discord account to your superium account first! sc!assign yourId')

@client.command()
async def trade(ctx):
    global tradeChannel
    tradeChannel = client.get_channel(750314777460473957)
    try:
        if type(userTable[ctx.author.name]) is int:
            embed = discord.Embed(description=f"{ctx.author.name} wants to trade. Use this link: https://superium.net/Trade/NewTrade?id={userTable[ctx.author.name]} ", title=f"A wild trade has appeared!",  colour=discord.Color.red())
            await tradeChannel.send(embed=embed)
    except KeyError:
        await ctx.send('assign your discord account to your superium account first! sc!assign yourId')

@client.command()
async def game(ctx, id):
    global gameLink
    gameChannel = client.get_channel(750314819160244234)
    try:
        if type(userTable[ctx.author.name]) is int:
            page = requests.get(gameLink + id).text
            soup = BeautifulSoup(page, "lxml")
            name = soup.find('h1', class_="title is-4")
            name = str(name).replace('<h1 class="title is-4">', '').replace('</h1>', '')

            author = re.sub(r'<a href="\/user\/[0-9]{1,4}">', '', str(soup.find('h1', 'subtitle is-6')).replace("Superium Game by", '').replace('<h1 class="subtitle is-6">', '').replace('</h1>', '').replace('</a>', '') )

            embed = discord.Embed(description=f"{name} by {author}", title=f"A wild game has appeared!",  colour=discord.Color.red())
            embed.set_thumbnail(url='https://superium.net/assets/thumbnails/games/' + str(id) + '.png')
            await gameChannel.send(embed=embed)
    except KeyError:
        await ctx.send('assign your discord account to your superium account first! sc!assign yourId')



client.run('NzUwMjIyMDg1MzU5NDAzMDU4.X03Yww.4H9HTegRzubqioYqyCTyodv5W64')