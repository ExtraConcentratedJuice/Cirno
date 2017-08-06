# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
import time
import os
import requests
import json
import time
from datetime import datetime, timedelta
import random
import re
import asyncio
from collections import Counter
    
class general():
	def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 15, type=commands.BucketType.channel)
    async def help(self,ctx):
        """Help command"""
        await self.bot.add_reaction(ctx.message, '\U0001F44C')
        embedhelp = discord.Embed(color = 0x870c0f, description = 'I am a gay multi-purpose Discord bot created by ExtraConcentratedJuice. Multi-purpose may be an overstatement though, because I am completely useless. Extra is absolutely terrible at code, so expect me to be mildly retarded at times.\n\nAll commands have a 3.5 second cooldown.\n\nCertain commands have been omitted from this manual due to their potential for abuse or their completely inane nature.') \
                    .set_author(name = '𝔗𝔥𝔢 𝔒𝔣𝔣𝔦𝔠𝔦𝔞𝔩 ℜ𝔬𝔟𝔬-𝔉ü𝔥𝔯𝔢𝔯 𝔐𝔞𝔫𝔲𝔞𝔩', url = 'https://harpy.cf', icon_url = self.bot.user.avatar_url) \
                    .set_thumbnail(url = 'https://i.imgur.com/qHytgB2.png') \
                    .add_field(name = "__**General Purpose**__", value = 'The usual commands. Satisfaction not guaranteed.', inline = False) \
                    .add_field(name = "``!rbhello``", value = 'Useless command that will work 100% of the time to check if the bot is alive.', inline = False) \
                    .add_field(name = "``!commonwords (#channel) (days) (number of words)``", value = 'Gives you a list of commonly used words in a channel, according to your parameters.', inline = False) \
                    .add_field(name = "``!robomusic``", value = 'Gives you MUSIC commands.', inline = False) \
                    .add_field(name = "``!gasjews``", value = 'Gas chamber meme.', inline = False) \
                    .add_field(name = "``!russianroulette``", value = 'Shoot yourself.', inline = False) \
                    .add_field(name = "``!dice``", value = 'Rolls a dice.', inline = False) \
                    .add_field(name = "``!doubledice``", value = 'Rolls TWO dice.', inline = False) \
                    .add_field(name = "``!coin``", value = 'Flips a coin, complete with image of a coin.', inline = False) \
                    .add_field(name = "``!kms``", value = 'Six different ways to express your loss of the will to live.', inline = False) \
                    .add_field(name = "``!roboinfo``", value = 'Gives you some information regarding this bot.', inline = False) \
                    .add_field(name ='__**Game Stuff**__', value = 'Stuff related to gaem\n', inline = False) \
                    .add_field(name = "``!stats (SteamID64 or Vanity URL)``", value = 'Gives you Unturned stats.', inline = False) \
                    .add_field(name = "``!steamid (Vanity URL)``", value = 'Converts a Vanity URL to SteamID64.', inline = False) \
                    .add_field(name ='__**Weeb Shit**__', value = 'Gay weeb commands. Why I even waste my time on this crap?\n', inline = False) \
                    .add_field(name = '``!animestream (name)``', value = 'Gives you an anime stream from twist.moe.', inline = False) \
                    .add_field(name = "``!animeimg (tag)``", value = 'Gives you an anime image with your tag.', inline = False) \
                    .add_field(name = "``!animeinfo (name)``", value = 'Gives you information about an anime.', inline = False) \
                    .add_field(name = "``!catgirl``", value = 'Gives you a catgirl.', inline = False) \
                    .add_field(name = "``!thicc``", value = 'T H I C C', inline = False) \
                    .add_field(name = "``!thighhighs``", value = 'Gives you thighhighs.', inline = False) \
                    .add_field(name = "``!weebsearch``", value = 'Weeaboo image search. !searchhelp for usage.', inline = False) \
                    .set_footer(text = 'Robo-Führer, by ExtraConcentratedJuice', icon_url = 'https://i.imgur.com/ItO8dUz.png')
        await self.bot.say(embed=embedhelp)
        
    

    @commands.command(pass_context=True)
    async def rfhello(self, ctx):
        """Check if the bot is alive."""
        
        await self.bot.say('Beep Boop. I am completely functional.')

    @commands.command(pass_context=True)
    async def kms(self, ctx):
        """SIX whole ways to express your loss of the will to live."""

        suicidemethods = [':gun:', ':pill:', ':dagger:', ':bomb:', ':syringe:']
        await self.bot.say(':grinning: ' + random.choice(suicidemethods))

    @commands.command(pass_context=True)
    async def coin(self, ctx):
        """Coinflip, with picture of coin."""

        heads = discord.Embed(title='Heads') \
        .set_image(url='http://i.magaimg.net/img/q1h.png')

        tails = discord.Embed(title='Tails') \
        .set_image(url='http://i.magaimg.net/img/q1i.png')
        
        await self.bot.say(embed=random.choice([heads, tails]))

    @commands.command(pass_context=True)
    async def dice(self, ctx):
        """Rolls a dice."""

        await self.bot.say('Roll: ``{}``'.format(random.randint(1, 6)))

    @commands.command(pass_context=True)
    async def doubledice(self, ctx):
        """Rolls TWO dice."""

        await self.bot.say('Roll: ``{}`` + ``{}``'.format(random.randint(1, 6), random.randint(1, 6)))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 13, type=commands.BucketType.channel)
    async def commonwords(self, ctx, channel, days : int, words : int):
        """Generates a list of common words in a channel."""
        
        channel = re.sub('[^0-9]', '', channel)
        if days > 7:
            await self.bot.say('You can only do up to a week\'s worth of messages.')
            return
        if words > 70:
            await self.bot.say('You can only do up to 70 words.')
            return
        
        await self.bot.say('``Gathering information...``')

        timestart = time.time()
        
        dateafter = datetime.now() - timedelta(days=int(days))

        wordlist = []

        chan = self.bot.get_channel(channel)
        
        async for message in self.bot.logs_from(chan, limit=1200, after=dateafter):
            if message.author.bot:
                continue
            if message.author == self.bot.user:
                continue
            cleanmsg = (message.clean_content).encode('ascii', 'ignore')
            wordlist.append(str(cleanmsg))

        wordlist = ''.join(wordlist)
            
        worddata = re.findall(r'\w+', wordlist)

        worddata = [word for word in worddata if len(word) > 3]

        worddata = [word.lower() for word in worddata]

        wordcount = Counter(worddata)

        countmsg = []

        for k, v in wordcount.most_common(words):
            countmsg.append('"' + k + '"' + ', ' + str(v) + ' times.')

        timeend = (time.time() - timestart)

        msg = '```Words processed in ' + str(round(timeend, 2)) + ' seconds.\n\n' + 'List of top ' + str(words) + ' commonly used words in #' + chan.name + ' in the past ' + str(days * 24) + ' hours:\n\n' + '\n'.join(countmsg)+ '```'

        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def russianroulette(self, ctx):
        """Russian Roulette."""
        bullet = random.randint(1,6)
        await self.bot.say(':gun: The chambers have been spun.')
        await asyncio.sleep(1.5)
        pulltrig = 'You pull the trigger, and...\n'
        if bullet == 1:
            await self.bot.say(pulltrig + ':tada: BANG!\nA bullet went straight into your head. lol')
        else:
            await self.bot.say(pulltrig + '*Click*\nYou live. At least for now.')

    @commands.command(pass_context=True)
    async def gasjews(self, ctx):
        """Gas chamber meme"""
        gasjews = ['http://i.magaimg.net/img/qsx.png', 'http://i.magaimg.net/img/q13.gif', 'http://i.magaimg.net/img/q14.png', 'http://i.magaimg.net/img/q5c.jpg']
        self.bot.say(random.choice(gasjews))

    @commands.command(pass_context=True)
    async def cat(self, ctx):
        kitty = requests.get('http://random.cat/meow')
        cat = kitty.json()
        catlink = (cat['file'])
        embed = discord.Embed(title='A cat from that shitty cat API').set_image(url=catlink)
        await self.bot.say(embed=embed)
        

def setup(bot):
    bot.add_cog(general(bot))
