# -*- coding: cp1252 -*-
from discord.ext import commands
import discord
import logging
import yaml

logging.basicConfig(level=logging.INFO)

main_cmd = ['cmds.botcontrol', 'cmds.anime', 'cmds.general', 'cmds.misc', 'cmds.games']

bot = commands.Bot(command_prefix ='!', description='Robo-Fuhrer but it\'s rewritten to be slightly less horrible')

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, '``Error | Missing argument(s).``')
    elif isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, '``Error | You\'ve used this command way too fast, try again in {} seconds.``'.format(round(error.retry_after, 2)))
    elif isinstance(error, commands.BadArgument):
        await bot.send_message(ctx.message.channel, '``Error | Bad argument(s).``')
    elif isinstance(error, commands.TooManyArguments):
        await bot.send_message(ctx.message.channel, '``Error | Too many arguments.``')
    else:
       print(type(error))
        
@bot.event
async def on_ready():
    print("RF BOOTING UP!")
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(game=discord.Game(name='the Holocaust', url="https://twitch.tv/meme", type=1))

with open("config.yaml", 'r') as f:
    config = yaml.load(f)

for module in main_cmd:
    try:
        bot.load_extension(module)
        print(str(module) + " successfully loaded.")
    except Exception as e:
        print(str(module) + " failed to load. | " + str(e))

bot.run(config['token'])
