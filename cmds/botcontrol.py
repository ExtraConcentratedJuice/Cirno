from discord.ext import commands
import discord
import yaml

class botcontrol():
    def __init__(self, bot):
        self.bot = bot

    with open("config.yaml", 'r') as f:
        config = yaml.load(f)

    owner = config['owner']

    @commands.command(pass_context=True)
    async def rfblacklist(self, ctx, *, user):
        """Lets you blacklist a user."""
        if ctx.message.author.id != self.owner:
            await self.bot.say('no ur gay')
            return
        
        if len(ctx.message.mentions) != 1:
            await self.bot.say('You\'re supposed to mention 1 user, retard.')
            return
        
        blackman = ''.join(ctx.message.mentions[0].id)
        bannedlist = open('blacklist.txt', 'r')
        bannedusers = bannedlist.read().splitlines()
        
        if blackman in bannedusers:
            await self.bot.say('This faggot is already blacklisted.')
            return

        bannedlist.close()

        bl = open('blacklist.txt', 'a')
        bl.write(blackman + '\n')
        bl.close()
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

        blackuser = ''.join(ctx.message.mentions[0].id)

        bannedlist = open('blacklist.txt', 'r')
        bannedusers = bannedlist.read().splitlines()
        
        if blackuser not in bannedusers:
            await self.bot.say('The user that you mentioned is not blacklisted.')
            return

        bannedlist.close()

        with open('blacklist.txt', 'r') as f:
            newbans = f.read().replace(blackuser + '\n', '')
            f.close()
        with open('blacklist.txt', "w+") as f:
            f.write(newbans)
            f.close()
        
        await self.bot.add_reaction(ctx.message, '\U0001F44C')
        await self.bot.say(ctx.message.mentions[0].mention + ' has been unblacklisted.')
            
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

def setup(bot):
    bot.add_cog(botcontrol(bot))
