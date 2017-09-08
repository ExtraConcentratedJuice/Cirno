# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
import time
import os
import requests
import json
import aiohttp
import time
from datetime import datetime, timedelta
import random
import re
import asyncio
from collections import Counter
import yaml

async def GET(url, params={}):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
    except:
        return None
    
    return data

with open("config.yaml", 'r') as f:
    config = yaml.load(f)

pr = config['prefix']
    
class general():
    
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, type=commands.BucketType.user)
    async def help(self,ctx):
        """Help command"""
        await self.bot.add_reaction(ctx.message, '\U0001F44C')
        #lol i need to fix the spacing
        embedhelp = discord.Embed(color = 0x870c0f, description = 'I am a gay multi-purpose Discord bot created by ExtraConcentratedJuice. Multi-purpose may be an overstatement though, because I am completely useless. Extra is absolutely terrible at code, so expect me to be mildly retarded at times.\n\nAll commands have a 3.5 second cooldown.\n\nCertain commands have been omitted from this manual due to their potential for abuse or their completely inane nature.') \
                    .set_author(name = '𝔗𝔥𝔢 𝔒𝔣𝔣𝔦𝔠𝔦𝔞𝔩 ℜ𝔬𝔟𝔬-𝔉ü𝔥𝔯𝔢𝔯 𝔐𝔞𝔫𝔲𝔞𝔩', url = 'https://harpy.cf', icon_url = self.bot.user.avatar_url) \
                    .set_thumbnail(url = 'https://i.imgur.com/qHytgB2.png') \
                    .add_field(name = "__**General Purpose**__", value = 'The usual commands. Satisfaction not guaranteed.', inline = False) \
                    .add_field(name = pr + "``rbhello``", value = 'Useless command that will work 100% of the time to check if the bot is alive.', inline = False) \
                    .add_field(name = pr + "``commonwords (#channel) (days) (number of words)``", value = 'Gives you a list of commonly used words in a channel, according to your parameters.', inline = False) \
                    .add_field(name = pr + "``reddit (subreddit, e.g. The_Donald)``", value = 'Grabs a post from the front page of the specified subreddit.', inline = False) \
                    .add_field(name = pr + "``gasjews``", value = 'Gas chamber meme.', inline = False) \
                    .add_field(name = pr + "``russianroulette``", value = 'Shoot yourself.', inline = False) \
                    .add_field(name = pr + "``dice``", value = 'Rolls a dice.', inline = False) \
                    .add_field(name = pr + "``doubledice``", value = 'Rolls TWO dice.', inline = False) \
                    .add_field(name = pr + "``coin``", value = 'Flips a coin, complete with image of a coin.', inline = False) \
                    .add_field(name = pr + "``kms``", value = 'Six different ways to express your loss of the will to live.', inline = False) \
                    .add_field(name = pr + "``roboinfo``", value = 'Gives you some information regarding this bot.', inline = False) \
                    .add_field(name ='__**Game Stuff**__', value = 'Stuff related to gaem\n', inline = False) \
                    .add_field(name = pr + "``stats (SteamID64 or Vanity URL)``", value = 'Gives you Unturned stats.', inline = False) \
                    .add_field(name = pr + "``query (x.x.x.x:12345)``", value = 'Queries and returns data about a source server. Works for other games, but tailored for Unturned.', inline = False) \
                    .add_field(name = pr + "``steamid (Vanity URL)``", value = 'Converts a Vanity URL to SteamID64.', inline = False) \
                    .add_field(name ='__**Weeb Shit**__', value = 'Gay weeb commands. Why I even waste my time on this crap?\n', inline = False) \
                    .add_field(name = pr + '``animestream (name)``', value = 'Gives you an anime stream from twist.moe.', inline = False) \
                    .add_field(name = pr + "``animeimg (tag)``", value = 'Gives you an anime image with your tag.', inline = False) \
                    .add_field(name = pr + "``animeinfo (name)``", value = 'Gives you information about an anime.', inline = False) \
                    .add_field(name = pr + "``catgirl``", value = 'Gives you a catgirl.', inline = False) \
                    .add_field(name = pr + "``thicc``", value = 'T H I C C', inline = False) \
                    .add_field(name = pr + "``thighhighs``", value = 'Gives you thighhighs.', inline = False) \
                    .add_field(name = pr + "``weebsearch (tag1 tag2 character_name)``", value = 'Weeaboo image search. Separate tags by spaces. Spaces in character names represented by an underscore.', inline = False) \
                    .add_field(name = pr + "``gelbooru (tag1 character_name)``", value = 'Same as weebsearch, just on Gelbooru.', inline = False) \
                    .set_footer(text = 'Robo-Führer, by ExtraConcentratedJuice', icon_url = 'https://i.imgur.com/ItO8dUz.png')
        embedhelp2 = discord.Embed(color = 0x870c0f, description = 'Page two of the offical Robo-Führer manual.') \
                    .set_author(name = '𝔗𝔥𝔢 𝔒𝔣𝔣𝔦𝔠𝔦𝔞𝔩 ℜ𝔬𝔟𝔬-𝔉ü𝔥𝔯𝔢𝔯 𝔐𝔞𝔫𝔲𝔞𝔩, pg2', url = 'https://harpy.cf', icon_url = self.bot.user.avatar_url) \
                    .set_thumbnail(url = 'https://i.imgur.com/qHytgB2.png') \
                    .add_field(name = "__**IMPORTANT**__", value = 'If you wish to enable the Führer\'s moderator log, create a channel named ``rf-logs`` and give RF permissions to write, read, and embed.', inline = False) \
                    .add_field(name = "__**Moderation**__", value = 'Administrative commands. You MUST be in a role named ``rf-moderator`` for the commands to work.', inline = False) \
                    .add_field(name = pr + "``purge (# of msgs)``", value = 'Purges the specified number of messages from the channel.', inline = False) \
                    .add_field(name = pr + "``softban (@user) (reason)``", value = 'Kicks a user and removes all their messages.', inline = False) \
                    .add_field(name = pr + "``kick (@user) (reason)``", value = 'Kicks a user from the server.', inline = False) \
                    .add_field(name = pr + "``ban (@user) (reason)``", value = 'Bans a user from the server.', inline = False) \
                    .add_field(name = "__**Misc.**__", value = 'All the other stuff.', inline = False) \
                    .add_field(name = pr + "``gibsauce``", value = 'Gives you Robo-Fuhrer\'s mess of a source code.', inline = False) \
                    .add_field(name = pr + "``invite``", value = 'Invite my useless ass to your server! You can have your VERY OWN Robo-Führer.', inline = False) \
                    .add_field(name = pr + "``server``", value = 'Gives information about the server that this command was run in.', inline = False) \
                    .add_field(name = pr + "``user (@user)``", value = 'Gives information about a mentioned user.', inline = False) \
                    .add_field(name = pr + "``reportissue (issue)``", value = 'Reports an issue. Suggestions are also welcome. If you misuse this command, you will be niggered.', inline = False) \
                    .set_footer(text= "Robo-Führer, by ExtraConcentratedJuice", icon_url = 'https://i.imgur.com/ItO8dUz.png')

        await self.bot.send_message(ctx.message.author, 'Hey, here\'s that help that you wanted.')
        await self.bot.send_message(ctx.message.author, embed=embedhelp)
        await self.bot.send_message(ctx.message.author, embed=embedhelp2)
        
    

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
    @commands.cooldown(1, 29, type=commands.BucketType.channel)
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
        
        async for message in self.bot.logs_from(chan, limit=45000, after=dateafter):
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

        try:
            await self.bot.say(msg)
        except:
            await self.bot.say('Message was too long, try a lower number of days.')

    @commands.command(pass_context=True)
    async def russianroulette(self, ctx):
        """Russian Roulette."""
        
        bullet = random.randint(1, 6)
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
        """Sends a cat from that shitty cat API"""
        
        kitty = requests.get('http://random.cat/meow')
        cat = kitty.json()
        catlink = (cat['file'])
        embed = discord.Embed(title='A cat from that shitty cat API').set_image(url=catlink)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def gibsauce(self, ctx):
        """Source code of bot"""
        
        await self.bot.say('https://github.com/ExtraConcentratedJuice/robo-fuhrer')

    @commands.command(pass_context=True)
    async def WEEB(self):
        """WEEBcoin stats"""

        data = await GET('http://159.203.169.234/api.php', {'q' : 'mining'})

        embed = discord.Embed(title='WeebCoin') \
                .set_footer(text='data is from kohai\'s gay api') \
                .set_image(url='http://i.magaimg.net/img/181l.jpg') \
                .add_field(name='Blocks', value=data['blocks'], inline=False) \
                .add_field(name='Current Block Size', value=data['currentblocksize'], inline=False) \
                .add_field(name='Current Block Difficulty', value=data['difficulty'], inline=False) \
                .add_field(name='Network Hashes / Second', value=data['networkhashps'], inline=False) \
                .add_field(name='Value', value='Zero (0) USD', inline=False)

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 8, type=commands.BucketType.channel)
    async def reddit(self, ctx, subreddit):
        """Get reddit posts from the front page of a subreddit."""

        #this is a mess, i'll have to redo it later

        is_nsfw = 'nsfw' in ctx.message.channel.name
        cleanurl = requests.compat.quote(subreddit)
        data = await GET('https://www.reddit.com/r/{}/about.json'.format(cleanurl))

        if data == None:
            await self.bot.say('Request failed.')
            return
        
        try:
            if data['kind'] == 'Listing':
                await self.bot.say('``/r/{}`` was not found.'.format(subreddit))
                return
        except KeyError:
            pass
            
        try:
            if data['error'] == 404:
                await self.bot.say('I didn\'t find shit. It is likely that ``/r/{}`` does not exist.'.format(subreddit))
                return
            
            if data['error'] == 403:
                try:
                    if data['reason'] == 'private':
                        await self.bot.say('``/r/{}`` is private; I can\'t retrieve posts from it.'.format(subreddit))
                        return
                except:
                    pass
                await self.bot.say('``/r/{}`` is quarantined. No way I am posting shit from there.'.format(subreddit))
                return
        except KeyError:
            pass

        if data['data']['over18'] and not is_nsfw:
            await self.bot.say('``/r/{}`` is an NSFW subreddit. Do that shit in an NSFW channel.'.format(subreddit))
            return

        subreddit = data['data']['url']

        data = await GET('https://www.reddit.com/r/{}/hot/.json'.format(cleanurl), {'limit' : '25'})
        #'len - 2' to account for some extra objects in 'children'
        postlen = len(data['data']['children']) - 2
        objectid = (random.randint(0, postlen))
        content = data['data']['children'][objectid]['data']

        while content['stickied']:
            if len(data['data']['children']) <= 2:
                break
            objectid = (random.randint(0, postlen))
            content = data['data']['children'][objectid]['data']


        url = 'https://reddit.com{}'.format(content['permalink'])
        embed = discord.Embed(title=content['title'], url=url, description=content['selftext'] if content['selftext_html'] else None) \
                .set_footer(text='{}, retrieved {}'.format(subreddit, time.strftime("%d/%m/%Y")), icon_url='http://i.magaimg.net/img/19y2.png')

        if content['thumbnail']:
            embed.set_image(url=content['thumbnail'])

        reg = re.compile('(\.png|\.jpg|\.gif|\.jpeg)')

        if not reg.search(content['url']):
            try:
                if content['media']['oembed']:
                    embed = discord.Embed(title=content['title'], url=url, description='\n[' + content['url'] + '](' + content['url'] + ')') \
                    .set_footer(text='{}, retrieved {}'.format(subreddit, time.strftime("%d/%m/%Y")), icon_url='http://i.magaimg.net/img/19y2.png')
                    embed.set_image(url=content['media']['oembed']['thumbnail_url'])
            except:
                pass

        if not content['media_embed'] and not content['is_self']:
            embed = discord.Embed(title=content['title'], url=url, description='\n[' + content['url'] + '](' + content['url'] + ')') \
            .set_footer(text='{}, retrieved {}'.format(subreddit, time.strftime("%m/%d/%Y")), icon_url='http://i.magaimg.net/img/19y2.png')

            if content['thumbnail']:
                embed.set_image(url=content['thumbnail'])

            if not reg.search(content['url']):
                try:
                    if content['media']['oembed']:
                        embed = discord.Embed(title=content['title'], url=url, description='\n[' + content['url'] + '](' + content['url'] + ')') \
                        .set_footer(text='{}, retrieved {}'.format(subreddit, time.strftime("%d/%m/%Y")), icon_url='http://i.magaimg.net/img/19y2.png')
                        embed.set_image(url=content['media']['oembed']['thumbnail_url'])
                except:
                    pass

        if content['is_self']:
            embed = discord.Embed(title=content['title'], url=url, description=content['selftext'] if content['selftext_html'] else None) \
            .set_footer(text='{}, retrieved {}'.format(subreddit, time.strftime("%d/%m/%Y")), icon_url='http://i.magaimg.net/img/19y2.png')
            

        #HOW DO I FIX THIS CODE HELP
            
        try:
            await self.bot.say(embed=embed)
        except:
            embed = discord.Embed(title=content['title'], url=url, description='Post content is too long. Please click on the link to view it in full.') \
            .set_footer(text='{}, retrieved {}'.format(subreddit, time.strftime("%m/%d/%Y")), icon_url='http://i.magaimg.net/img/19y2.png')
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(general(bot))
