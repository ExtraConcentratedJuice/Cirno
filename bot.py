from discord.ext import commands
import discord
import logging
import yaml
import sqlite3

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
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
       print(type(error) + ' ' + str(error))

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

    #checks if blacklist database exists, creates one if it doesn't
    db = sqlite3.connect('data/banned.db')
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT)')
    db.commit()
    db.close()

with open("config.yaml", 'r') as f:
    config = yaml.load(f)

for module in main_cmd:
    try:
        bot.load_extension(module)
        print(str(module) + " successfully loaded.")
    except Exception as e:
        print(str(module) + " failed to load. | " + str(e))

bot.run(config['token'])
