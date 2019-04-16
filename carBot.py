import random
from discord.ext import commands
import discord
import time

token = 'NTY0NDQxMjAzNTkzMDUyMTgw.XKttpA.hHp8b9GMYrsDmzYIXNoYLNRburw'

bot = commands.Bot(command_prefix='!', status=discord.Status.idle, activity=discord.Game(name='Booting'))
bot.remove_command('help')


@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'My ping is {bot.latency}')


@bot.command()
async def babka(ctx):
    await ctx.channel.send(f'My ping is {}')


@bot.command()
async def ban(ctx, member:discord.User = None, reason = None):
    if member == None or member == ctx.message.author or member.name == 'Carrbot#5579':
        await ctx.channel.send("You cannot ban yourself!")
        return
    if reason == None:
        reason = "No reason at all!"
    message = f"You have been banned from {ctx.guild.name} for {reason}!"
    await member.send(message)
    await ban()
    await ctx.channel.send(f"{member} is banned!")


@bot.command()
async def rndm(ctx, a, b):
    await ctx.channel.send(str(random.randint(int(a),int(b))))

bot.run(token)
