# -*- coding: utf-8 -*-
"""
Module for other stuff.
"""
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
        """Servers"""
        
        await self.bot.say(len(self.bot.servers))

    @commands.command(pass_context=True)
    async def server(self, ctx):
        "Server info command"""
        
        embed = discord.Embed(color=0x870c0f, title=ctx.message.server.name) \
        .set_thumbnail(url=(ctx.message.server.icon_url).replace('jpg', 'png')) \
        .add_field(name='Owner', value=str(ctx.message.server.owner), inline=False) \
        .add_field(name='Created', value=str(ctx.message.server.created_at), inline=False) \
        .add_field(name='Members', value=str(ctx.message.server.member_count), inline=False) \
        .add_field(name='ID', value=str(ctx.message.server.id), inline=False) \
        .add_field(name='Region', value=str(ctx.message.server.region), inline=False)

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def user(self, ctx):
        "User info command"""

        if len(ctx.message.mentions) != 1:
            await self.bot.say('You need to mention ``1`` user to retrieve info from.')
            return

        usrinf = ctx.message.mentions[0]
        
        embed = discord.Embed(color=0x870c0f, title=usrinf.name + '#' + str(usrinf.discriminator)) \
        .set_thumbnail(url=(usrinf.avatar_url).replace('jpg', 'png')) \
        .add_field(name='Nickname', value=str(usrinf.display_name), inline=False) \
        .add_field(name='Joined', value=str(usrinf.created_at), inline=False) \
        .add_field(name='ID', value=str(usrinf.id), inline=False) \

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def reportissue(self, ctx, *, issue):
        embed = discord.Embed(description=issue) \
        .set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url) \
        .add_field(name='Server: ', value=ctx.message.server.name) \
        .add_field(name='Channel: ', value=ctx.message.channel.id)
        
        await self.bot.send_message(self.bot.get_channel('338421643879645186'), embed=embed)
        await self.bot.add_reaction(ctx.message, '\U0001F44C')

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        """Invite link"""
        
        await self.bot.say('https://discordapp.com/oauth2/authorize?client_id=338414455291510785&scope=bot&permissions=201850055')


def setup(bot):
    bot.add_cog(misc(bot))
