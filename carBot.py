import random
from discord.ext import commands
import discord
import time

token = 'NTY0NDQxMjAzNTkzMDUyMTgw.XKttpA.hHp8b9GMYrsDmzYIXNoYLNRburw'

bot = commands.Bot(command_prefix='!', status=discord.Status.idle, activity=discord.Game(name='Booting'))
bot.remove_command('help')


@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'My ping is {bot.latency * 1000}')


@bot.command()
async def rndm(ctx, a, b):
    await ctx.channel.send(str(random.randint(int(a),int(b))))

bot.run(token)
