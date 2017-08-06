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


def setup(bot):
    bot.add_cog(misc(bot))
