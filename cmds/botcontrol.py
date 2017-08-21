from discord.ext import commands
import discord
import yaml
import sqlite3

class botcontrol():
    def __init__(self, bot):
        self.bot = bot

    with open("config.yaml", 'r') as f:
        config = yaml.load(f)

    owner = config['owner']

    @commands.command(pass_context=True)
    async def rfblacklisted(self, ctx):
        """Prints all blacklisted users."""
        if ctx.message.author.id != self.owner:
            return
        
        db = sqlite3.connect('data/banned.db')
        c = db.cursor()

        c.execute("SELECT * FROM users")

        ulist = []
        for user in c.fetchall():
            ulist.append('ID: {}, NAME: {}'.format(user[0], user[1]))
            
        db.close()
        await self.bot.say('```Blacklisted Users:\n\n{}```'.format('\n'.join(ulist)))
        
    @commands.command(pass_context=True)
    async def rfblacklist(self, ctx, *, user):
        """Lets you blacklist a user."""
        
        if ctx.message.author.id != self.owner:
            await self.bot.say('no ur gay')
            return
        
        if len(ctx.message.mentions) != 1:
            await self.bot.say('You\'re supposed to mention 1 user, retard.')
            return
        
        db = sqlite3.connect('data/banned.db')
        c = db.cursor()
        c.execute('SELECT * FROM users WHERE id= ?', (ctx.message.mentions[0].id,))
        
        if c.fetchone() != None:
            db.close()
            await self.bot.say('This faggot is already blacklisted.')
            return

        c.execute('INSERT INTO users(id, name) VALUES(?,?)', (ctx.message.mentions[0].id, ctx.message.mentions[0].name))
        db.commit()
        db.close()
        await self.bot.add_reaction(ctx.message, '\U0001F44C')
        await self.bot.say('I no longer take orders from that faggot ' + ctx.message.mentions[0].mention + '.')

    @commands.command(pass_context=True)
    async def rfunblacklist(self, ctx, *, module):
        """Unblacklists a user."""
        
        if ctx.message.author.id != self.owner:
            await self.bot.say('no ur gay')
            return
        
        if len(ctx.message.mentions) != 1:
            await self.bot.say('You\'re supposed to mention 1 user, retard.')
            return

        db = sqlite3.connect('data/banned.db')
        c = db.cursor()
        c.execute('SELECT * FROM users WHERE id= ?', (ctx.message.mentions[0].id,))
        
        if c.fetchone() == None:
            db.close()
            await self.bot.say('That user does not seem to be blacklisted.')
            return

        c.execute('DELETE FROM users WHERE id = ?', (ctx.message.mentions[0].id,))
        db.commit()
        db.close()
        await self.bot.add_reaction(ctx.message, '\U0001F44C')
        await self.bot.say(ctx.message.mentions[0].mention + ' has been removed from the blacklist.')
        
    @commands.command(pass_context=True)
    async def rfreload(self, ctx, *, module):
        """Lets you reload a command module."""
        if ctx.message.author.id != self.owner:
            return
        
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('Module failed to reload. | ' + str(e))
        else:
            await self.bot.say('Module successfully reloaded. | ' + module)
            
    @commands.command(pass_context=True)
    async def rfload(self, ctx, *, module):
        """Lets you load a command module."""
        if ctx.message.author.id != self.owner:
            return
        
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('Module failed to load. | ' + str(e))
        else:
            await self.bot.say('Module successfully loaded. | ' + module)
            
    @commands.command(pass_context=True)
    async def rfunload(self, ctx, *, module):
        """Lets you unload a command module."""
        if ctx.message.author.id != self.owner:
            return
        
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('Module failed to unload. | ' + str(e))
        else:
            await self.bot.say('Module successfully unloaded. | ' + module)

    @commands.command(pass_context=True)
    async def changestatus(self, ctx, *, status):
        """Change bot status"""
        
        if ctx.message.author.id != self.owner:
            return
        await self.bot.change_presence(game=discord.Game(name=status, url="https://twitch.tv/meme", type=1))

def setup(bot):
    bot.add_cog(botcontrol(bot))
