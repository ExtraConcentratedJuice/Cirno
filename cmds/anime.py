# -*- coding: utf-8 -*-
"""
Module for anime related commands.

TO DO:

Add manga stuff
MAL user profile stuff
Improve animestreams/themes

"""
from discord.ext import commands
import discord
import json
import re
from bs4 import BeautifulSoup
import random
import distance
import requests
from urllib.parse import quote
import yaml
import bleach
import aiohttp
import time
import asyncio
import sqlite3
import spice_api as spice
import textwrap



class anime():
    
    def __init__(self, bot):
        self.bot = bot

    async def fetchlist(self, service, params):
        """post list request function"""
        
        if service == 'yandere':
            url = 'https://yande.re/post.json'
        elif service == 'danbooru':
            url = 'https://danbooru.donmai.us/posts.json'
        elif service == 'gelbooru':
            url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1'
        else:
            raise ValueError('Invalid service. Must be yandere, danbooru, or gelbooru.')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    images = await resp.json()
        except:
            raise SystemError('Request failed.')
        
        return images

    with open("config.yaml", 'r') as f:
        config = yaml.load(f)
        
    creds = spice.init_auth(config['MALAuth']['username'], config['MALAuth']['password'])

    @commands.command(pass_context=True)
    @commands.cooldown(5, 6, type=commands.BucketType.channel)
    async def animeimg(self, ctx, *, imgtag):
        """Gives you an anime image."""

        params = {'tags' : imgtag + ' rating:safe', 'limit' : 5, 'random' : 'true'}
        
        try:
            imagelist = await self.fetchlist('danbooru', params)
        except SystemError:
            await self.bot.send_message(ctx.message.channel, '``An internal error has occurred.``')
            return

        if len(imagelist) == 0:
            await self.bot.say('No images were found for ``{}``. Try another tag.'.format(imgtag))
            return
        
        try:
            img = random.choice(imagelist)
        except KeyError:
            await self.bot.say('Danbooru has a limitation on tags. Please use only one tag.')
            return
        
        animeimg = ("https://danbooru.donmai.us{}".format(img['file_url']))
        embed = discord.Embed(title='tag: '+imgtag) \
        .set_image(url=animeimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(5, 6, type=commands.BucketType.channel)
    async def hentaiimg(self, ctx, *, imgtag):
        """No."""
        
        params = {'tags' : imgtag + ' rating:explicit', 'limit' : 5, 'random' : 'true'}
        
        if 'nsfw' not in ctx.message.channel.name:
            await self.bot.say('You must be in a channel with ``nsfw`` in it\'s name to use this command.')
            return
        
        try:
            imagelist = await self.fetchlist('danbooru', params)
        except SystemError:
            await self.bot.send_message(ctx.message.channel, '``An internal error has occurred.``')
            return
        
        if len(imagelist) == 0:
            await self.bot.say('No images were found for ``{}``. Try another tag.'.format(imgtag))
            return
        
        try:
            img = random.choice(imagelist)
        except KeyError:
            await self.bot.say('Danbooru has a limitation on tags. Please use only one tag.')
            return

        hentaiimg = ("https://danbooru.donmai.us{}".format(img['file_url']))
        
        embed = discord.Embed(title='tag: '+imgtag) \
        .set_image(url=hentaiimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, type=commands.BucketType.user)
    async def hentaibomb(self, ctx, *, imgtag):
        """No."""
        
        params = {'tags' : imgtag + ' rating:explicit', 'limit' : 10, 'random' : 'true'}
        await self.bot.add_reaction(ctx.message, '\U0001F44C')

        try:
            images = await self.fetchlist('danbooru', params)
        except SystemError:
            await self.bot.send_message(ctx.message.channel, '``An internal error has occurred.``')
            return

        if len(images) == 0:
            await self.bot.say('No images found for ``{}``. Try another tag?'.format(imgtag))
            return
        
        try:
            images[0]
        except:
            await self.bot.say('Danbooru has a limitation on tags. Please use only one tag.')
            return

        iterations = (10 - random.randint(3, 9))
        del images[-iterations:]

        for i in images:
            try:
                img = random.choice(images)
                himg = ("http://danbooru.donmai.us{0}".format(i['file_url']))
            except:
                continue
                
            embed = discord.Embed(title='tag: ' + imgtag) \
            .set_image(url=himg) \
            .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
            await self.bot.send_message(ctx.message.author, embed=embed)
            
        await self.bot.say('Check your inbox for some fresh hentai, '+ ctx.message.author.mention + '.')

    @commands.command(pass_context=True)
    @commands.cooldown(3, 3, type=commands.BucketType.channel)
    async def thighhighs(self, ctx):
        """OH YEAH, THIGHHIGHS!"""

        params = {'tags' : 'thighhighs rating:safe', 'limit' : 5, 'random' : 'true'}
        
        imagelist = await self.fetchlist('danbooru', params)
        img = random.choice(imagelist)
        animeimg = ("https://danbooru.donmai.us{}".format(img['file_url']))
        
        embed = discord.Embed(title='thighhighs') \
        .set_image(url=animeimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(3, 3, type=commands.BucketType.channel)
    async def catgirl(self, ctx):
        """The best things in the universe."""

        params = {'tags' : 'cat_girl rating:safe', 'limit' : 5, 'random' : 'true'}
        catgirlmessage= ['KITTY!', 'nyaa~', 'here\'s your fucking 2d catgirl', 'catgirl', 'nekomimi', 'stop looking for catgirls weeb']
        
        imagelist = await self.fetchlist('danbooru', params)
        img = random.choice(imagelist)
        animeimg = ("https://danbooru.donmai.us{}".format(img['file_url']))
        
        embed = discord.Embed(title=random.choice(catgirlmessage)) \
        .set_image(url=animeimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=embed)
    @commands.command(pass_context=True)
    @commands.cooldown(3, 3, type=commands.BucketType.channel)
    async def thicc(self, ctx):
        """T H I C C bitches"""

        params = {'tags' : 'curvy rating:safe', 'limit' : 5, 'random' : 'true'}

        imagelist = await self.fetchlist('danbooru', params)
        img = random.choice(imagelist)
        thiccimg = ("https://danbooru.donmai.us{}".format(img['file_url']))
        
        thiccembed = discord.Embed(title='T H I C C') \
        .set_image(url=thiccimg) \
        .set_footer(text='https://danbooru.donmai.us', icon_url='http://i.imgur.com/4Wjm9rb.png')
        await self.bot.say(embed=thiccembed)

    @commands.command(pass_context=True)
    @commands.cooldown(2, 5, type=commands.BucketType.channel)
    async def weebsearch(self, ctx, *, imgtags):
        """A command to search for stuff on the yande.re imageboard."""
        
        if 'nsfw' not in ctx.message.channel.name:
            imgtags = imgtags.replace(' rating:explicit', '').replace(' rating:questionable', '')
            imgtags = (imgtags + ' rating:safe')
            
        params = {'tags' : imgtags, 'limit' : 10, 'page' : random.randint(1, 12)}
        images = await self.fetchlist('yandere', params)
        if len(images) == 0:
            params = {'tags' : imgtags, 'limit' : 10, 'page' : '1'}
            images = await self.fetchlist('yandere', params)
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
    @commands.cooldown(2, 6, type=commands.BucketType.channel)
    async def gelbooru(self, ctx, *, imgtags):
        """A command to search for stuff on the Gelbooru imageboard."""

        if 'nsfw' not in ctx.message.channel.name:
            imgtags = imgtags.replace(' rating:explicit', '').replace(' rating:questionable', '')
            imgtags = (imgtags + ' rating:safe')

        try:
            params = {'tags' : imgtags, 'limit' : 25, 'pid' : (random.randint(1, 10))}
            images = await self.fetchlist('gelbooru', params)
            if len(images) == 0:
                raise ValueError('No images found.')
        except:
            try:
                params = {'tags' : imgtags, 'limit' : 30}
                images = await self.fetchlist('gelbooru', params)
                
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
                    break

        if '.webm' in img['file_url']:
            await self.bot.say('Discord doesn\'t support webms in embeds, and it looks like there were no other images that aren\'t webms. Here is the image that was found:\n\nhttp:{}'.format(img['file_url']))
            return
        
        weebimg = img['file_url']
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

        stream_success = False
        db = sqlite3.connect('data/data.db')
        c = db.cursor()
        c.execute('SELECT time FROM data')
        
        try:
            lastupdated = c.fetchone()[0]
        except (IndexError, TypeError):
            lastupdated = 0
            
        if (time.time() - lastupdated) > 86400:
            await self.bot.say('``Cached list is out of date, retrieving new information and updating database.``')
            
            async with aiohttp.ClientSession() as session:
                async with session.get('https://twist.moe') as resp:
                    alist = await resp.text()
                
            animeweb = BeautifulSoup(alist, 'lxml')
            animelist = animeweb.find_all("a", class_="series-title")
            c.execute('DELETE FROM data')
            db.commit()
            c.execute('VACUUM')
            db.commit()
            
            for a in animelist:
                try:
                    element = {'href' : a['href'], 'data_title' : a['data-title'], 'data_alt' : a['data-alt'], 'time' : time.time()}
                except KeyError:
                    element = {'href' : a['href'], 'data_title' : a['data-title'], 'data_alt' : None, 'time' : time.time()}
                c.execute('INSERT INTO data(href, data_title, data_alt, time) VALUES(?,?,?,?)', (element['href'], element['data_title'], element['data_alt'], element['time']))

            db.commit()
            print('List Updated.')
            
        try:
            animeinfo = spice.search(animename, spice.get_medium('anime'), self.creds)
            animetitle = animeinfo[0].title
            animethumb = animeinfo[0].image_url
        except IndexError:
            await self.bot.say('No such anime seems to exist. Not in the MAL database, at least.')
            return

        c.execute('SELECT * FROM data')
        animelinks = {}
        
        for a in c.fetchall():
            animelinks[a[1]] = a[0]

        animelink = animelinks.get(animetitle.lower())
        stream_success = True
        
        if animelink is None:
            stream_success = False
            for k, v in animelinks.items():
                if distance.levenshtein(animetitle.lower(), k.lower()) < 2:
                    animelink = v
                    #Fix for "second season" anime titles, so you don't get season one.
                    if k.lower() != animetitle.lower():
                        for k, v in animelinks.items():
                            if animetitle.lower() == k.lower():
                                animelink = v
                    stream_success = True
                    break
            
        if not stream_success:
            c.execute('SELECT * FROM data')
            animelinks = {}
            
            for a in c.fetchall():
                animelinks[a[2]] = a[0]
                
            for k, v in animelinks.items():
                try:
                    if distance.levenshtein(animetitle.lower(), k.lower()) < 2:
                        animelink = v
                        if k.lower() != animetitle.lower():
                            for k, v in animelinks.items():
                                if animetitle.lower() == k.lower():
                                    animelink = v
                        stream_success = True
                        break
                except AttributeError:
                    continue

            if not stream_success:
                htmlurl = quote(animetitle, safe='')
                await self.bot.say('The anime (*' + animetitle + '*) does not seem to exist in the twist.moe streams.\n\nHere are some pages pointing to what you might be looking for:\n\n__**Nyaa**__\n\nhttps://nyaa.pantsu.cat/search?c=_&userID=0&q=' + htmlurl + '\n\n__**Gayanime**__\n\nhttp://kissanime.ru/Search/Anime?keyword=' + htmlurl)
                return

        db.close()
        twistembed = discord.Embed(title=animetitle, url='https://twist.moe' + animelink, description='Click on the link above for a highly illegal anime stream!', color=10038562).set_thumbnail(url=animethumb).set_footer(text='twist.moe')
        await self.bot.say(embed=twistembed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, type=commands.BucketType.channel)
    async def animetheme(self, ctx, *, animename):
        
        theme_success = False

        db = sqlite3.connect('data/data.db')
        c = db.cursor()
        c.execute('SELECT time FROM op_data')
        
        try:
            lastupdated = c.fetchone()[0]
        except (IndexError, TypeError):
            lastupdated = 0
            
        if (time.time() - lastupdated) > 86400:
            await self.bot.say('``Cached list is out of date, retrieving new information and updating database.``')
            
            async with aiohttp.ClientSession() as session:
                async with session.get('https://themes.moe/includes/anime_live_search.json?') as resp:
                    themelist = await resp.json()

            c.execute('DELETE FROM op_data')
            db.commit()
            c.execute('VACUUM')
            db.commit()
            
            for a in themelist:
                try:
                    element = {'id' : a['i'], 'data_title' : a['c'], 'data_alt' : a['e'], 'time' : time.time()}
                except KeyError:
                    element = {'id' : a['i'], 'data_title' : a['c'], 'data_alt' : None, 'time' : time.time()}
                    
                c.execute('INSERT INTO op_data(id, data_title, data_alt, time) VALUES(?,?,?,?)', (element['id'], element['data_title'], element['data_alt'], element['time']))

            db.commit()
            print('Theme List Updated.')

        try:
            animeinfo = spice.search(animename, spice.get_medium('anime'), self.creds)
            animetitle = animeinfo[0].title
            animethumb = animeinfo[0].image_url
        except IndexError:
            await self.bot.say('No such anime seems to exist. Not in the MAL database, at least.')
            return

        c.execute('SELECT * FROM op_data')
        themedata = {}
        
        for a in c.fetchall():
            themedata[a[1].lower()] = a[0]

        themelink = themedata.get(animetitle.lower())
        theme_success = True
        
        if themelink is None:
            theme_success = False
            for k, v in themedata.items():
                #Levenshtein comparison to account for small errors in names.
                #It works fast enough, I think it's worth using.
                if distance.levenshtein(animetitle.lower(), k.lower()) < 2:
                    themelink = v
                    if k.lower() != animetitle.lower():
                        for k, v in themedata.items():
                            if animetitle.lower() == k.lower():
                                themelink = v
                    theme_success = True
                    break

        if not theme_success:
            c.execute('SELECT * FROM op_data')
            themelinks = {}
            
            for a in c.fetchall():
                themelinks[a[2]] = a[0]
                
            for k, v in themelinks.items():
                try:
                    if distance.levenshtein(animetitle.lower(), k.lower()) < 2:
                        themelink = v
                        if k.lower() != animetitle.lower():
                            for k, v in animelinks.items():
                                if animetitle.lower() == k.lower():
                                    themelink = v
                        theme_success = True
                        break
                except AttributeError:
                    continue

        if not theme_success:
            self.bot.say('No themes found for the anime ``{}``.'.format(animetitle))
            return

        try:
            async with aiohttp.ClientSession() as session:
                    async with session.post('https://themes.moe/includes/anime_search.php', data={'search' : themelink}) as resp:
                        page = await resp.text()
        except:
            await self.bot.say('Request to themes.moe failed. Try again later.')
            return

        db.close()
        page = re.sub(r'(?:((\\\\)*)\\)(?![\\{u])', '', page)
        page = BeautifulSoup(page, 'lxml')
        atitle = page.find('a', {'class' : 'mal-url'}).text
        alink = page.findAll('a', {'class' : 'mal-url'})[0]['href']
        #themes.moe escapes unicode
        atitle = bytes(atitle, 'utf8').decode('unicode_escape')
        
        embed = discord.Embed(title=atitle, url=alink, description='List of themes for ' + atitle) \
        .set_thumbnail(url=animethumb) \
        .set_footer(text='https://themes.moe')
        
        for v in page.findAll('a', {'class' : 'vid-popup'}):
            embed.add_field(name = v['data-type'], value='[{}]({})'.format(v['href'], v['href']), inline=False)

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, type=commands.BucketType.channel)
    async def touhou(self, ctx, *, twohu):
        """Grabs an entry from the Touhou wiki"""

        #lol 'structured progamming' who needs that
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://en.touhouwiki.net/api.php', params={'format' : 'json', 'action' : 'opensearch', 'search' : twohu}) as resp:
                    search = await resp.json()
        except:
            await self.bot.say('Request failed. Try again later.')
            return

        if len(search[1]) == 0:
            await self.bot.say('Nothing was found on the Touhou wiki for ``{}``.'.format(twohu))
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://en.touhouwiki.net/index.php', params={'title' : search[1][0], 'mobileaction' : 'toggle_view_mobile'}) as resp:
                    page = await resp.text()
        except:
            await self.bot.say('Request failed. Try again later.')
            return
        
        page = BeautifulSoup(page, 'lxml')
        contentdiv = page.find('div', {'class' : 'mf-section-0'})

        try:
            mainimage = contentdiv.find('a', {'class' : 'image'}).find('img')
        except:
            mainimage = None
            
        summary = contentdiv.find_all('p')[-1]
        
        try:
            name = contentdiv.find('th', {'class' : 'vcard; incell_top'}).contents[2]
        except:
            name = None

        try:
            name = name.text
        except:
            pass
            
        embed = discord.Embed(title=name if name != None else search[1][0], description=summary.text, url=search[3][0])
        if mainimage != None:
            embed.set_image(url='https://en.touhouwiki.net{}'.format(mainimage['src']))
            
        embed.set_footer(text='Information scraped from https://en.touhouwiki.net', icon_url='http://i.imgur.com/aLMipX6.png')
        
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(anime(bot))
