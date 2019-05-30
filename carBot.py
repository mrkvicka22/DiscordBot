from random import shuffle, randint

import discord
from discord.ext import commands

token = ...

bot = commands.Bot(command_prefix='!', status=discord.Status.idle, activity=discord.Game(name='Booting'))
bot.remove_command('help')

roles = {5:['liberal', 'liberal', 'liberal', 'hitler', 'facist'],
         6:['liberal', 'liberal', 'liberal', 'liberal','hitler','facist'],
         7:['liberal', 'liberal', 'liberal', 'liberal', 'hitler', 'facist', 'facist'],
         8:['liberal', 'liberal', 'liberal', 'liberal', 'liberal', 'hitler', 'facist', 'facist'],
         9:['liberal', 'liberal', 'liberal', 'liberal', 'liberal', 'hitler', 'facist', 'facist', 'facist'],
         10:['liberal', 'liberal', 'liberal', 'liberal', 'liberal', 'liberal', 'hitler', 'facist', 'facist', 'facist']
         }


class Shitler():

    def __init__(self, participants):
        self.players = participants


class Player():

    def __init__(self, role, disc_usr):
        self.role = role
        self.dsc_cls = disc_usr


@bot.command()
async def shitlerstart(ctx):
    parts = []
    if 11 > len(player_list) > 4:
        mix_roles = shuffle(roles[len(player_list)])
        for i in range(len(player_list)):
            parts.append(Player(mix_roles[i], player_list[i]))
        game = Shitler(parts)
        await ctx.channel.send('Game initialized')
    else:
        await ctx.channel.send('Not enough players have joined or too many players have joined')
        return 0


@bot.command()
async def shitlerjoin(ctx):
    player_list.append(ctx.message.author)
    await ctx.channel.send(f'Player {ctx.message.author} has joined the game')

in_progress = False


@bot.command()
async def shitlercreate(ctx):
    global in_progress
    if in_progress:
        await ctx.channel.send('The game is already in progress wait for it to finish!')
        return 0
    else:
        global player_list
        player_list = []
        in_progress = False
        await ctx.channel.send('The game created waiting for players to join')


@bot.command()
async def rndm(ctx,  a, b):
    author = ctx.message.author
    await author.send(str(randint(int(a),int(b))))

bot.run(token)
