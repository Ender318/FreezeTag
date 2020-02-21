import discord
import random
import time
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
client = discord.Client()
players = []
inThisGuild = []

# enters a user into the game; assigns Tag Player Role
@bot.command(name='joinGame')
async def join(ctx):
    user = ctx.message.author.id
    guild = ctx.message.guild.id
    inThisGuild.append(user)
    players.append(user)
    playersList = 'Players:', players
    player = ctx.message.author
    role = discord.utils.get(ctx.guild.roles, name='Tag Player')
    await player.add_roles(role)
    response = 'You joined the game'
    await ctx.send(response)

# returns the status of a user
@bot.command(name='status')
async def statux(ctx):
    users = ctx.message.mentions
    for i in users:
        user = discord.utils.get(ctx.message.mentions)
        status = user.status
        await ctx.send(status)

# freezes a user if the command user is it
@bot.command(name='tag')
async def tag(ctx):
    roles = ctx.message.author.roles
    it = discord.utils.get(ctx.guild.roles, name='It')
    tagPlayer = discord.utils.get(ctx.guild.roles, name='Tag Player')
    if tagPlayer in roles:
        if it in roles:
            player = discord.utils.get(ctx.message.mentions)
            frozen = discord.utils.get(ctx.guild.roles, name='Frozen')
            await player.add_roles(frozen)
        else:
            pass
    else:
        pass

# unfreezes players if command user isn't it or frozen
@bot.command(name='unfreeze')
async def unfreeze(ctx):
    roles = ctx.message.author.roles
    it = discord.utils.get(ctx.guild.roles, name='It')
    frozen = discord.utils.get(ctx.guild.roles, name='Frozen')
    tagPlayer = discord.utils.get(ctx.guild.roles, name='Tag Player')
    if tagPlayer in roles:
        if it in roles:
            message = 'You can\'t unfreeze someone!'
            await ctx.send(message)
            pass
        elif frozen in roles:
            pass
        else:
            player = discord.utils.get(ctx.message.mentions)
            await player.remove_roles(frozen)
    else:
        pass

# returns a list of players
@bot.command(name='players')
async def player(ctx):
    for i in inThisGuild:
        player = players[i].name
        await ctx.send(player)

# returns the latency of the bot
@bot.command(name='ping')
async def ping(ctx):
    ping = bot.latency
    await ctx.send(ping)

# returns the rules
@bot.command(name='rules')
async def rules(ctx):
    message = '```Rules: \n1. Only tag people that are online\n2. test```'
    await ctx.send(message)



bot.run('TOKEN')
