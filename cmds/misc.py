# -*- coding: cp1252 -*-
from discord.ext import commands
import discord

class misc():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(3, 8, type=commands.BucketType.channel)
    async def roboinfo(self, ctx):
        """Info command"""
        
        msg = '\n```Robo-Führer is a discord bot written in Python created by ExtraConcentratedJuice to boost the autism of discord servers. \n\ndiscord.py: 0.16.8\n\nPython: 3.6.1\n\nThe anime grill in the profile picture: Cave from Hyperdimension Neptunia\n\n!roboservers: All servers this bot is in.\n!robousers: How many users this bot is serving.```'
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def robousers(self, ctx):
        "User count command"""
        
        membercount = 0
        
        for server in self.bot.servers:
            membercount += server.member_count
            
        await self.bot.say('Robo-Führer is currently serving ``' + str(membercount) + '`` autistic children.')

    @commands.command(pass_context=True)
    async def roboservers(self, ctx):
        "Server list command"""
        
        rbservers = ['\n```List of servers Robo-Führer is in:']
        
        for server in self.bot.servers:
           rbservers.append(server.name)
           
        rbservers.append('```')
        await self.bot.say('\n'.join(rbservers))

    @commands.command(pass_context=True)
    async def server(self, ctx):
        "Server info command"""
        
        embed = discord.Embed(color = 0x870c0f, title = ctx.message.server.name) \
                      .set_thumbnail(url= (ctx.message.server.icon_url).replace('jpg', 'png')) \
                      .add_field(name = 'Owner', value = str(ctx.message.server.owner), inline = False) \
                      .add_field(name = 'Created', value = str(ctx.message.server.created_at), inline = False) \
                      .add_field(name = 'Members', value = str(ctx.message.server.member_count), inline = False) \
                      .add_field(name = 'ID', value = str(ctx.message.server.id), inline = False) \
                      .add_field(name = 'Region', value = str(ctx.message.server.region), inline = False)

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def user(self, ctx):
        "User info command"""

        if len(ctx.message.mentions) != 1:
            await client.send_message(message.channel, 'You need to mention ``1`` user to retrieve info from.')
            return

        usrinf = ctx.message.mentions[0]
        
        embed = discord.Embed(color = 0x870c0f, title = usrinf.name + str(usrinf.discriminator)) \
                      .set_thumbnail(url= (usrinf.avatar_url).replace('jpg', 'png')) \
                      .add_field(name = 'Nickname', value = str(usrinf.display_name), inline = False) \
                      .add_field(name = 'Joined', value = str(usrinf.created_at), inline = False) \
                      .add_field(name = 'ID', value = str(usrinf.id), inline = False) \

        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(misc(bot))
