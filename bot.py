# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
import aiohttp
import asyncio
import logging
import yaml
import sqlite3

logging.basicConfig(level=logging.INFO)

with open("config.yaml", 'r') as f:
    config = yaml.load(f)

main_cmd = ['cmds.botcontrol', 'cmds.anime', 'cmds.general', 'cmds.misc', 'cmds.games', 'cmds.moderation']
bot = commands.Bot(command_prefix=config['prefix'], description='Robo-Fuhrer but it\'s rewritten to be slightly less horrible')
logs = []

async def post_botlist():
    await bot.wait_until_ready()
    while not bot.is_closed:
        serverlen = len(bot.servers)
        headers = {'Authorization': config['discord_bots_token']}
        data = {'server_count': serverlen}
        url = 'https://discordbots.org/api/bots/{}/stats'.format(config['bot_client_id'])
        
        async with aiohttp.ClientSession() as session:
            await session.post(url, data=data, headers=headers)
            
        headers = {'Authorization': config['discord_pw_token']}
        data = {'server_count': serverlen}
        url = 'https://bots.discord.pw/api/bots/{}/stats'.format(config['bot_client_id'])
        
        async with aiohttp.ClientSession() as session:
            await session.post(url, data=data, headers=headers)
            
        print('Successfully sent server count to botlist!')
        await asyncio.sleep(1800)

async def dump_logs():
    #Dumps logs to .txt every 10 minutes
    await bot.wait_until_ready()
    while not bot.is_closed:
        log = open("log.txt", "a", encoding='utf8')
        for logdata in logs:
            log.write(logdata + '\n')
        log.close()
        logs.clear()
        await asyncio.sleep(600)
        

@bot.event
async def on_message(message):
    if message.content.startswith(config['prefix']) and config['enable_command_logging'] == 'True':
        logtxt = ("[{0}] [{1}] [{2}] {3}: {4}").format(message.timestamp, message.server, message.channel, message.author, message.clean_content)
        logs.append(logtxt)

    await bot.process_commands(message)
    
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, '``Error | Missing argument(s). Please refer to {}help for usage.``'.format(config['prefix']))
    elif isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, '``Error | This command was used way too fast, try again in {} seconds.``'.format(round(error.retry_after, 2)))
    elif isinstance(error, commands.BadArgument):
        await bot.send_message(ctx.message.channel, '``Error | Bad argument(s).``')
    elif isinstance(error, commands.TooManyArguments):
        await bot.send_message(ctx.message.channel, '``Error | Too many arguments.``')
    elif isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(str(error))

@bot.check
def is_blacklisted(ctx):
    """Checks if a user is blacklisted or not."""
    
    try:
        db = sqlite3.connect('data/banned.db')
        c = db.cursor()
        c.execute('SELECT * FROM users WHERE id= ?', (ctx.message.author.id,))
        
        if c.fetchone() != None:
            db.close()
            return False
        else:
            db.close()
            return True
        
    except:
        db.close()
        return True
        
@bot.event
async def on_ready():
    print("RF BOOTING UP!")
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(game=discord.Game(name='the Holocaust', url="https://twitch.tv/meme", type=1))

    if config['enable_command_logging'] == 'True':
        bot.loop.create_task(dump_logs())

    if config['enable_botlist'] == 'True':
        bot.loop.create_task(post_botlist())

    #creates databases
    db = sqlite3.connect('data/banned.db')
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT)')
    db.commit()
    db.close()
    
    db = sqlite3.connect('data/data.db')
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data(href TEXT PRIMARY KEY, data_title TEXT, data_alt TEXT, time REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS op_data(id TEXT PRIMARY KEY, data_title TEXT, data_alt TEXT, time REAL)')
    db.commit()
    db.close()

for module in main_cmd:
    try:
        bot.load_extension(module)
        print(str(module) + " successfully loaded.")
    except Exception as e:
        print(str(module) + " failed to load. | " + str(e))

bot.run(config['token'])
