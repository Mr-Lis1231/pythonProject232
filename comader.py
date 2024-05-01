import asyncio
import discord
import wikipedia
from discord.ext import commands
import random, logging
import requests
import json

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


class RandomThings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='кубик')
    async def roll_dice(self, ctx, count):
        res = [random.choice(dashes) for _ in range(int(count))]
        await ctx.send(" ".join(res))

    @commands.command(name='число')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)


    @commands.command(name='вики')
    async def my_randint(self, ctx, quer):
        wikipedia.set_lang('ru')
        res = wikipedia.search(quer)
        if not res:
            await ctx.send('No results found.')
        else:
            page = wikipedia.page(res[0])
            await ctx.send(page.url)




    @commands.command(name='wiki')
    async def my_wiki(self, ctx, quer):
        wikipedia.set_lang('en')
        res = wikipedia.search(quer)
        if not res:
            await ctx.send('No results found.')
        else:
            page = wikipedia.page(res[0])
            await ctx.send(page.url)

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(name='обнять')
    async def obnal(self, ctx, member: discord.Member = None):

        if member == None:
            return

        await ctx.channel.send(f"{ctx.author.mention} обнял {member.mention}")


bot = commands.Bot(command_prefix='/', intents=intents)

TOKEN = "MTIzMTI1MTM4MDAxNDk0NDMwNg.GWQgwE.ZESx61HZYKhLpm4MK4pCpKf2E-z10owOR2lm9Y"


async def main():
    await bot.add_cog(RandomThings(bot))
    await bot.start(TOKEN)


asyncio.run(main())