import random
from discord.ext import commands
import discord
import time

token = 'NTY0NDQxMjAzNTkzMDUyMTgw.XKttpA.hHp8b9GMYrsDmzYIXNoYLNRburw'

bot = commands.Bot(command_prefix='!', status=discord.Status.idle, activity=discord.Game(name='Booting'))
bot.remove_command('help')

game_is_ongoing = False

class Shitler():

    def __init__(self, participants):
        self.players = participants

class Player():
    
    def __init__(self, role, disc_usr):
        self.role = role
        self.dsc_cls = disc_usr

@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'My ping is {bot.latency * 1000}')


@bot.command()
async def shitler(ctx, *args):
    players = []
    for player in args:
        if isinstance(player, discord.User):
            players.append(player)

    shitler_game = Shitler(players)
    await ctx.channel.send('The game has been set up')


@bot.command(pass_context=True)
async def create(ctx):
    if game_is_ongoing:
        await ctx.channel.send('The game is already in progress wait for it to finish!')
        return 0
    global player_list
    player_list = []

@bot.command()
async def rndm(ctx,  a, b):
    author = ctx.message.author
    await author.send(str(random.randint(int(a),int(b))))

bot.run(token)
