# -*- coding: cp1252 -*-
from discord.ext import commands
import discord
import json
import re
from bs4 import BeautifulSoup
import random
import distance
from urllib.parse import quote
import yaml
import bleach
import aiohttp
import pickle
import time
import asyncio
#hehe xD le api wrapper
import spice_api as spice
from pybooru import Danbooru, Moebooru, PybooruHTTPError
import textwrap



class anime():
    
    def __init__(self, bot):
        self.bot = bot

    with open("config.yaml", 'r') as f:
        config = yaml.load(f)
        
    creds = spice.init_auth(config['MALAuth']['username'], config['MALAuth']['password'])

    moebooru = Moebooru('yandere')
    danbooru = Danbooru('danbooru')

    @commands.command(pass_context=True)
    @commands.cooldown(5, 6, type=commands.BucketType.channel)
    async def animeimg(self, ctx, *, imgtag):
        """Gives you an anime image."""

        try:
            imagelist = self.danbooru.post_list(tags=(imgtag + ' rating:safe'), limit=5, random=True)
        except PybooruHTTPError:
            await self.bot.say('Danbooru has a limitation on tags. Please use only one tag.')
            return
        
        if len(imagelist) == 0:
            await self.bot.say('No images were found for ``{}``. Try another tag.'.format(imgtag))
            return

        img = random.choice(imagelist)
        animeimg = ("http://danbooru.donmai.us{}".format(img['file_url']))
            
        embed = discord.Embed(title='tag: '+imgtag) \
        .set_image(url=animeimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(5, 6, type=commands.BucketType.channel)
    async def hentaiimg(self, ctx, *, imgtag):
        """No."""
        
        if 'nsfw' not in ctx.message.channel.name:
            await self.bot.say('You must be in a channel with ``nsfw`` in it\'s name to use this command.')
            return
        
        try:
            imagelist = self.danbooru.post_list(tags=(imgtag + ' rating:explicit'), limit=5, random=True)
        except PybooruHTTPError:
            await self.bot.say('Danbooru has a limitation on tags. Please use only one tag.')
            return
        
        if len(imagelist) == 0:
            await self.bot.say('No images were found for ``{}``. Try another tag.'.format(imgtag))
            return
            
        img = random.choice(imagelist)
        hentaiimg = ("http://danbooru.donmai.us{}".format(img['file_url']))
            
        embed = discord.Embed(title='tag: '+imgtag) \
        .set_image(url=hentaiimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 12, type=commands.BucketType.channel)
    async def hentaibomb(self, ctx, *, imgtag):
        """No."""
        
        await self.bot.add_reaction(ctx.message, '\U0001F44C')

        for i in range(random.randint(3, 9)):
            try:
                images = self.danbooru.post_list(tags=imgtag + ' rating:explicit', limit=10, random=True, page=random.randint(1,11))
            except PybooruHTTPError:
                await self.bot.say('Danbooru has a limitation on tags. Please use only one tag.')
                return
                
            if len(images) == 0:
                images = self.danbooru.post_list(tags=imgtag + ' rating:explicit', limit=9, random=True, page=1)
                if len(images) == 0:
                    await self.bot.say('No images found for ``{}``. Try another tag?'.format(imgtag))
                    return
            try:
                img = random.choice(images)
                himg = ("http://danbooru.donmai.us{0}".format(img['file_url']))
            except KeyError:
                continue
                               
            embed = discord.Embed(title='tag: ' + imgtag) \
            .set_image(url=himg) \
            .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
            await self.bot.send_message(ctx.message.author, embed=embed)
        await self.bot.send_message(ctx.message.channel, 'Check your inbox for some fresh hentai, '+ ctx.message.author.mention + '.')

    @commands.command(pass_context=True)
    @commands.cooldown(5, 3, type=commands.BucketType.channel)
    async def thighhighs(self, ctx):
        """OH YEAH, THIGHHIGHS!"""
        
        imagelist = self.danbooru.post_list(tags='thighhighs rating:safe', limit=5, random=True)
            
        img = random.choice(imagelist)
        animeimg = ("http://danbooru.donmai.us{}".format(img['file_url']))
            
        embed = discord.Embed(title='thighhighs') \
        .set_image(url=animeimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(5, 3, type=commands.BucketType.channel)
    async def catgirl(self, ctx):
        """The best things in the universe."""

        catgirlmessage= ['KITTY!', 'nyaa~', 'here\'s your fucking 2d catgirl', 'catgirl', 'nekomimi', 'stop looking for catgirls weeb']

        imagelist = self.danbooru.post_list(tags='cat_girl rating:safe', limit=5, random=True, page=random.randint(1, 30))
            
        img = random.choice(imagelist)
        animeimg = ("http://danbooru.donmai.us{}".format(img['file_url']))
            
        embed = discord.Embed(title=random.choice(catgirlmessage)) \
        .set_image(url=animeimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=embed)
    @commands.command(pass_context=True)
    @commands.cooldown(5, 3, type=commands.BucketType.channel)
    async def thicc(self, ctx):
        """The best things in the universe."""

        thicc = self.moebooru.post_list(tags='cleavage ass rating:safe order:score', limit=4, page=(random.randint(1, 35)))

        img = random.choice(thicc)
        thiccimg = ("{0}".format(img['file_url']))
            
        thiccembed = discord.Embed(title='T H I C C') \
        .set_image(url=thiccimg) \
        .set_footer(text='https://yande.re', icon_url='http://i.imgur.com/jemLswy.png')
        await self.bot.say(embed=thiccembed)

    @commands.command(pass_context=True)
    @commands.cooldown(5, 5, type=commands.BucketType.channel)
    async def weebsearch(self, ctx, *, imgtags):
        """A command to search for stuff on the yande.re imageboard."""

        if 'nsfw' not in ctx.message.channel.name:
            imgtags = imgtags.replace(' rating:explicit', '').replace(' rating:questionable', '')
            imgtags = (imgtags + ' rating:safe')

        images = self.moebooru.post_list(tags=imgtags, limit=8, page=(random.randint(1, 15)))
        if len(images) == 0:
            images = self.moebooru.post_list(tags=imgtags, limit=8, page=1)
            if len(images) == 0:
                await self.bot.say('No images found for the tags: ``{}``. Try some other tags?'.format(imgtags))
                return
            
        img = random.choice(images)
        weebimg = ("{}".format(img['file_url']))
        weebembed = discord.Embed(title='tags: ' + imgtags, description='``' + textwrap.fill(weebimg, 30) + '``') \
        .set_image(url=weebimg) \
        .set_footer(text='https://yande.re', icon_url='http://i.imgur.com/jemLswy.png')
        await self.bot.say(embed=weebembed)


    @commands.command(pass_context=True)
    @commands.cooldown(1, 6, type=commands.BucketType.channel)
    async def gelbooru(self, ctx, *, imgtags):
        """A command to search for stuff on the yande.re imageboard."""

        if 'nsfw' not in ctx.message.channel.name:
            imgtags = imgtags.replace(' rating:explicit', '').replace(' rating:questionable', '')
            imgtags = (imgtags + ' rating:safe')

        params = {'tags' : imgtags, 'limit' : 25, 'pid' : (random.randint(1, 10))}
        try:
            async with aiohttp.get('https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1', params=params) as r:
                images = await r.text()
                images = json.loads(images)
            if len(images) == 0:
                raise ValueError('No images found.')
        except:
            try:
                params = {'tags' : imgtags, 'limit' : 30}
                async with aiohttp.get('https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1', params=params) as r:
                    images = await r.text()
                    images = json.loads(images)
                if len(images) == 0:
                    raise ValueError('No images found.')
            except:
                await self.bot.say('No images found for the tags: ``{}``. Try some other tags?'.format(imgtags))
                return


        img = random.choice(images)
        #fix for webm. faggots at discord need to support webm NOW
        if '.webm' in img['file_url']:
            for image in images:
                if '.webm' in image['file_url']:
                    continue
                else:
                    img = image

        if '.webm' in img['file_url']:
            await self.bot.say('Discord doesn\'t support webms in embeds, and it looks like there were no other images that aren\'t webms. Here is the image that was found:\n\nhttp:{}'.format(img['file_url']))
            return
        
        weebimg = ("https:{0}".format(img['file_url']))
        weebembed = discord.Embed(title='tags: ' + imgtags, description='``' + textwrap.fill(weebimg, 38) + '``') \
        .set_image(url=weebimg) \
        .set_footer(text='https://gelbooru.com', icon_url='http://i.imgur.com/UVGcJdK.png')
        await self.bot.say(embed=weebembed)

    @commands.command(pass_context=True)
    @commands.cooldown(2, 10, type=commands.BucketType.channel)
    async def animeinfo(self, ctx, *, animename):
        """Gets you anime info from MAL"""
        
        sanime = spice.search(animename, spice.get_medium('anime'), self.creds)
        #unnecessary vars, too lazy to change from my old code though
        animeid = sanime[0].id
        animetitle = sanime[0].title
        animedesc = sanime[0].synopsis
        animedesc = bleach.clean(animedesc, tags=[], attributes={}, styles=[], strip=True)
        animedesc = animedesc.replace('[i]', '').replace('[/i]', '')
        #just cleans the description from the escapes and bbshit
        animeep = sanime[0].episodes
        if animeep == '0':
            animeep = 'Airing'
        animetype = sanime[0].anime_type
        animeairing = sanime[0].status
        animepic = sanime[0].image_url
        animedate = sanime[0].dates
        animedates = animedate[0]
        animedatee = animedate[1]
        if animedatee == '0000-00-00':
            animedatee = 'N/A'
        animeinfo = discord.Embed(title=animetitle, description=animedesc).set_thumbnail(url=animepic).add_field(name='Type:', inline=True, value = animetype).add_field(name='Episodes:', value = animeep).add_field(name='Aired:', inline=True, value = animedates).add_field(name='Finished Airing:', inline=True, value = animedatee).set_footer(text=('Information fetched from the MyAnimeList API:\nhttps://myanimelist.net/anime/'+animeid),icon_url='https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png')
        await self.bot.say(embed=animeinfo)

    @commands.command(pass_context=True)
    @commands.cooldown(3, 8, type=commands.BucketType.channel)
    async def animestream(self, ctx, *, animename):
        """Gets you an illegal anime stream"""
        
        #i should probably fix this shitcode sooner or later
        
        stream_success = False
        try:
            animeinfo = spice.search(animename, spice.get_medium('anime'), self.creds)
            animetitle = animeinfo[0].title
            animethumb = animeinfo[0].image_url
        except IndexError:
            await self.bot.say('No such anime seems to exist. Not in the MAL database, at least.')
            return
        
        try:
            oldtime = pickle.load(open('timeinfo', 'rb'))
        except:
            async with aiohttp.get('https://twist.moe') as r:
                alist = await r.text()
            f = open('twistlist.html', 'w')
            f.write(alist.encode('ascii', 'ignore').decode('ascii'))
            f.close
            pickle.dump(time.time(), open('timeinfo', 'wb'))

        if (time.time() - oldtime) > 43200:
            async with aiohttp.get('https://twist.moe') as r:
                alist = await r.text()
            f = open('twistlist.html', 'w')
            f.write(alist.encode('ascii', 'ignore').decode('ascii'))
            f.close
            pickle.dump(time.time(), open('timeinfo', 'wb'))
            print('LIST UPDATED')

        f = open('twistlist.html', 'r')
        animeweb = f.read()
        animeweb = BeautifulSoup(animeweb, 'lxml')
        f.close()
        animelist = animeweb.find_all("a", class_="series-title")
        animelinks = {}
        
        for item in animelist:
            animelinks[item['data-title']] = item['href']
            
        for k, v in animelinks.items():
            if distance.levenshtein(animetitle.lower(), k.lower()) < 4:
                animelink = v
                stream_success = True
                break
            
        if stream_success == False:
            animelinks = {}
            for item in animelist:
                try:
                    animelinks[item['data-alt']] = item['href']
                except KeyError:
                    continue
                
            for k, v in animelinks.items():
                if distance.levenshtein(animetitle.lower(), k.lower()) < 4:
                    animelink = v
                    stream_success = True
                    break

            if stream_success == False:
                htmlurl = quote(animetitle, safe='')
                await self.bot.say('The anime (*' + animetitle + '*) does not seem to exist in the twist.moe streams.\n\nHere are some pages pointing to what you might be looking for:\n\n__**Nyaa**__\n\nhttps://nyaa.pantsu.cat/search?c=_&userID=0&q=' + htmlurl + '\n\n__**Gayanime**__\n\nhttp://kissanime.ru/Search/Anime?keyword=' + htmlurl)
                return
                
        twistembed = discord.Embed(title=animetitle, url='https://twist.moe' + animelink, description='Click on the link above for a highly illegal anime stream!', color=10038562).set_thumbnail(url=animethumb).set_footer(text='twist.moe')
        await self.bot.say(embed=twistembed)
            
def setup(bot):
    bot.add_cog(anime(bot))
