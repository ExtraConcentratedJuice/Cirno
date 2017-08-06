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
