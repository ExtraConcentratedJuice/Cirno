# -*- coding: cp1252 -*-
from discord.ext import commands
import discord

class moderation():
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 4, type=commands.BucketType.channel)
    async def purge(self, ctx, number):
        """Purges messages from a chat channel."""
        
        userPerms = discord.utils.get(ctx.message.author.roles, name='rf-moderator')
        
        if userPerms == None:
            await self.bot.say('Insufficient permissions. You must be in a role named ``rf-moderator`` in order to execute this command.')
            return

        try:
            number = int(number)
        except:
            await self.bot.say('``ERROR | Bad value.``')

        try:
            await self.bot.purge_from(channel=ctx.message.channel, limit=number)
        except discord.Forbidden:
            await self.bot.say('Failed to purge. Robo-Führer has insufficient privileges.')
            return

        await self.bot.say('{} messages removed from {}. I hope that wasn\'t a mistake.'.format(str(number), ctx.message.channel.mention))


    @commands.command(pass_context=True)
    @commands.cooldown(1, 4, type=commands.BucketType.channel)
    async def ban(self, ctx, user, *, banreason):
        """Ban a user"""
        
        userPerms = discord.utils.get(ctx.message.author.roles, name='rf-moderator')
        
        if userPerms == None:
            await self.bot.say('Insufficient permissions. You must be in a role named ``rf-moderator`` in order to execute this command.')
            return

        if len(ctx.message.mentions) != 1:
            await self.bot.say('You need to mention ``1`` user to ban.')
            return

        user = ctx.message.mentions[0]
        
        try:
            await self.bot.ban(user, delete_message_days=7)
        except discord.Forbidden:
            await self.bot.say('Failed to ban. Robo-Führer has insufficient privileges.')
            return

        await self.bot.say('The specified user has been banned.')

        try:
            logchannel = discord.utils.get(self.bot.get_all_channels(), server__id=ctx.message.server.id, name='rf-logs')
        except:
            return

        try:
            embed = discord.Embed(color = 0x870c0f) \
                        .set_author(name='User: ' + user.name, icon_url=user.avatar_url) \
                        .add_field(name='Type', value='Ban', inline=False) \
                        .add_field(name='Reason', value=banreason, inline=False) \
                        .add_field(name='Issuer', value=ctx.message.author.name, inline=False)
            await self.bot.send_message(logchannel, embed=embed)
        except:
            await self.bot.say('Logging to ``rf-logs`` failed! Make sure the bot has write, read, and embed permissions!')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 4, type=commands.BucketType.channel)
    async def kick(self, ctx, user, *, kickreason):
        """Kick a user"""
        
        userPerms = discord.utils.get(ctx.message.author.roles, name='rf-moderator')
        
        if userPerms == None:
            await self.bot.say('Insufficient permissions. You must be in a role named ``rf-moderator`` in order to execute this command.')
            return

        if len(ctx.message.mentions) != 1:
            await self.bot.say('You need to mention ``1`` user to ban.')
            return

        user = ctx.message.mentions[0]
        
        try:
            await self.bot.kick(user)
        except discord.Forbidden:
            await self.bot.say('Failed to kick. Robo-Führer has insufficient privileges.')
            return

        await self.bot.say('The specified user has been kicked.')

        try:
            logchannel = discord.utils.get(self.bot.get_all_channels(), server__id=ctx.message.server.id, name='rf-logs')
        except:
            return

        try:
            embed = discord.Embed(color = 0x870c0f) \
                        .set_author(name='User: ' + user.name, icon_url=user.avatar_url) \
                        .add_field(name='Type', value='Kick', inline=False) \
                        .add_field(name='Reason', value=kickreason, inline=False) \
                        .add_field(name='Issuer', value=ctx.message.author.name, inline=False)
            await self.bot.send_message(logchannel, embed=embed)
        except:
            await self.bot.say('Logging to ``rf-logs`` failed! Make sure the bot has write, read, and embed permissions!')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 4, type=commands.BucketType.channel)
    async def softban(self, ctx, user, *, banreason):
        """Softbans a user. Bans, unbans so they're 'kicked' with all of their messages being deleted."""
        
        userPerms = discord.utils.get(ctx.message.author.roles, name='rf-moderator')
        
        if userPerms == None:
            await self.bot.say('Insufficient permissions. You must be in a role named ``rf-moderator`` in order to execute this command.')
            return

        if len(ctx.message.mentions) != 1:
            await self.bot.say('You need to mention ``1`` user to ban.')
            return

        user = ctx.message.mentions[0]
        
        try:
            await self.bot.ban(user, delete_message_days=7)
            await self.bot.unban(user.server, user)
        except discord.Forbidden:
            await self.bot.say('Failed to ban. Robo-Führer has insufficient privileges.')
            return

        await self.bot.say('The specified user has been softbanned.')

        try:
            logchannel = discord.utils.get(self.bot.get_all_channels(), server__id=ctx.message.server.id, name='rf-logs')
        except:
            return

        try:
            embed = discord.Embed(color = 0x870c0f) \
                        .set_author(name='User: ' + user.name, icon_url=user.avatar_url) \
                        .add_field(name='Type', value='Softban', inline=False) \
                        .add_field(name='Reason', value=banreason, inline=False) \
                        .add_field(name='Issuer', value=ctx.message.author.name, inline=False)
            await self.bot.send_message(logchannel, embed=embed)
        except:
            await self.bot.say('Logging to ``rf-logs`` failed! Make sure the bot has write, read, and embed permissions!')
            
def setup(bot):
    bot.add_cog(moderation(bot))
