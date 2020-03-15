import discord
import time
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
client = discord.Client()
players = []
playersid = []
tagged = []


# starts the game timer
@bot.command(name='startGame')
async def start(ctx):
    gameManager = discord.utils.get(ctx.guild.roles, name='Game Manager')
    roles = ctx.message.author.roles
    global time1
    bool = False
    while True:
        for i in roles:
            if i == gameManager:
                time1 = time.time()
                bool = True
                break
            else:
                pass
        if bool:
            break
        else:
            message = 'Only the Game Manager can start the game.'
            await ctx.send(message)

    for i in range(players.__len__()):
        player = players[i]
        it = discord.utils.get(ctx.guild.roles, name='It')
        for role in player.roles:
            if role == it:
                del playersid[i]
                break
            else:
                pass
    playersid.sort()


# enters a user into the game; assigns Tag Player Role
@bot.command(name='joinGame')
async def join(ctx):
    player = ctx.message.author
    players.append(player)
    playersid.append(player.id)
    role = discord.utils.get(ctx.guild.roles, name='Tag Player')
    await player.add_roles(role)
    response = 'You joined the game'
    await ctx.send(response)


# freezes a user if the command user is it
@bot.command(name='tag')
async def tag(ctx):
    roles = ctx.message.author.roles
    it = discord.utils.get(ctx.guild.roles, name='It')
    tagPlayer = discord.utils.get(ctx.guild.roles, name='Tag Player')

    # checks if the tag is legal
    if tagPlayer in roles:
        if it in roles:
            player = discord.utils.get(ctx.message.mentions)
            if tagPlayer in player.roles:
                if player.status == discord.Status.online:
                    frozen = discord.utils.get(ctx.guild.roles, name='Frozen')
                    await player.add_roles(frozen)
                    tagged.append(player.id)
                    tagged.sort()
                    if playersid == tagged:
                        ctx.message.author.add_roles(frozen)
                        await endGame(ctx)
                    else:
                        pass
                else:
                    message = 'You can only tag someone who is online!'
                    await ctx.send(message)
            else:
                message = 'You can only tag someone who is playing the game!'
                await ctx.send(message)
        else:
            message = 'You can only tag someone if you are it!'
            await ctx.send(message)
    else:
        message = 'You must be playing the game to participate!'
        await ctx.send(message)


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


# ends the game
async def endGame(ctx):
    global time2
    time2 = time.time()
    global gameTime
    gameTime = time2 - time1
    hours = gameTime // 3600
    minutes = gameTime // 60
    seconds = gameTime % 3600
    message = 'The game time was ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' \
                                                                              '' + str(seconds) + ' seconds.'
    await ctx.send(message)

    tagPlayer = discord.utils.get(ctx.guild.roles, name='Tag Player')
    frozen = discord.utils.get(ctx.guild.roles, name='Frozen')
    for i in range(players.__len__()):
        player = players[i]
        player.remove_roles(tagPlayer)
        player.remove_roles(frozen)
    players.clear()
    playersid.clear()


# returns the status of a user
@bot.command(name='status')
async def statux(ctx):
    users = ctx.message.mentions
    for i in users:
        user = discord.utils.get(ctx.message.mentions)
        status = user.status
        await ctx.send(status)


# returns the latency of the bot
@bot.command(name='ping')
async def ping(ctx):
    ping = bot.latency
    await ctx.send(ping)


# returns the rules
@bot.command(name='rules')
async def rules(ctx):
    message = '```Rules: \n1. Only tag people that are online\n2. Only tag people playing the game. ' \
              'This runs on mentions so don\'t spam others\n3. Do not use an invisible status to hide: that is cheating\n' \
              '4. Do not join the game late, it will mess up the times\n' \
              '5. The time starts when an admin uses the start game command\n' \
              '\n**HOW TO PLAY**\n' \
              'This game is tournament style. Everyone playing takes turns being \"it\". After everyone has taken ' \
              'their turn, the person with the fastest time to end the game is the winner.```'
    await ctx.send(message)


bot.run('TOKEN')
