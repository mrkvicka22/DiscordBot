from random import shuffle, randint

import discord
from discord.ext import commands

token = 'NTY0NDQxMjAzNTkzMDUyMTgw.XKttpA.hHp8b9GMYrsDmzYIXNoYLNRburw'

bot = commands.Bot(command_prefix='!', status=discord.Status.idle, activity=discord.Game(name='Booting'))
bot.remove_command('help')

game_is_ongoing = False

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


@bot.command()
async def shitlercreate(ctx):
    global game_is_ongoing
    if game_is_ongoing:
        await ctx.channel.send('The game is already in progress wait for it to finish!')
        return 0

    global player_list
    player_list = []
    game_is_ongoing = True


@bot.command()
async def rndm(ctx,  a, b):
    author = ctx.message.author
    await author.send(str(randint(int(a),int(b))))

bot.run(token)
