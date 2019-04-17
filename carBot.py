import random
from discord.ext import commands
import discord
import time

token = 'NTY0NDQxMjAzNTkzMDUyMTgw.XKttpA.hHp8b9GMYrsDmzYIXNoYLNRburw'

bot = commands.Bot(command_prefix='!', status=discord.Status.idle, activity=discord.Game(name='Ressurecting Hitler. Using TOP SECRET encryption. Victim not known.'))
bot.remove_command('help')


class Shitler():

    def __init__(self, participants):
        self.players = participants
        
        
@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'My ping is {bot.latency * 1000}')


@bot.command()
async def channel(ctx, chaname):
    guild = ctx.message.guild
    await guild.create_text_channel(chaname)

@bot.command()
async def shitler(ctx, *args):
    players = []
    for player in args:
        if isinstance(player, discord.User):
            players.append(a)

    shitler_game = Shitler(players)
    await ctx.channel.send(f'My ping is {bot.latency * 1000}')


@bot.command()
async def rndm(ctx, a, b):
    await ctx.channel.send(str(random.randint(int(a),int(b))))

bot.run(token)
