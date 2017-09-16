# -*- coding: utf-8 -*-
"""
Module for game related commands.

TO DO:

CS:GO Stats/Items

"""
import re
import aiohttp
import discord
from discord.ext import commands
import yaml
from bs4 import BeautifulSoup
from urllib.parse import quote
import steam
import valve.source.a2s

async def parse_item_data(query):
    """parse html data"""
    
    url = 'https://steamcommunity.com/market/search/render/search'
    params = {'appid' : '304930', 'query' : query, 'start' : 0, 'count' : 100}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
    except:
        return False

    if not data['success']:
        return False

    if data['total_count'] == 0:
        return None

    item = {}
    html = data['results_html']
    html = re.sub(r'(?:((\\\\)*)\\)(?![\\{u])', '', html)
    content = BeautifulSoup(html, 'lxml')
    rows = content.find_all('div', {'class' : 'market_listing_row'})
    page = None

    for r in rows:
        if r.find('span', {'market_listing_item_name'}).text.lower() == query.lower():
            page = r
            break

    if page is None:
        page = content.find('div', {'class' : 'market_listing_row'})
        
    item['Name'] = page.find('span', {'class' : 'market_listing_item_name'}).text
    item['img_url'] = page.find('img')['src']
    item['url_enc'] = quote(item['Name'], safe='')

    for i in page.find_all('span', {'class' : 'normal_price'}):
        if len(i['class']) == 1:
            item['Price'] = i.text
            break

    return item

class games():
    def __init__(self, bot):
        self.bot = bot

    with open("config.yaml", 'r') as f:
        config = yaml.load(f)
        
    steam.api.key.set(config['steamkey'])
    osukey = config['osukey']
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 8, type=commands.BucketType.channel)
    async def stats(self, ctx, player):
        """Gets you those Unturned stats."""
        
        try:
            steamid = steam.user.vanity_url('https://steamcommunity.com/id/' + player)
            player = steamid.id64
        except steam.user.VanityError:
            pass
        
        try:
            profile = steam.user.profile(str(player))
            utstats = steam.api.interface('ISteamUserStats').GetUserStatsForGame(appid=304930, steamid=int(player))
            steamname = (profile.persona)
            
            playerskilled = (utstats['playerstats']['stats']['Kills_Players']['value'])
            zombieskilled = (utstats['playerstats']['stats']['Kills_Zombies_Normal']['value'])
            megaskilled = (utstats['playerstats']['stats']['Kills_Zombies_Mega']['value'])
            playerdeaths = (utstats['playerstats']['stats']['Deaths_Players']['value'])
            killdeath = round(playerskilled/playerdeaths, 2)
            shotstaken = (utstats['playerstats']['stats']['Accuracy_Shot']['value'])
            shotshit = (utstats['playerstats']['stats']['Accuracy_Hit']['value'])
            accuracy = round(shotshit/shotstaken * 100, 2)
            arenawins = (utstats['playerstats']['stats']['Arena_Wins']['value'])
            headshotshit = (utstats['playerstats']['stats']['Headshots']['value'])
            headshotrate = round(headshotshit/shotshit * 100, 2)
            #SHIT that is one long ass string, I need to go and fix this crap later.
            msg = '\n```Unturned Statistics\n\n\nPlayer Name: ' + steamname + "\nSteamID64: " + str(player) + "\n\n--- Kills & Deaths ---\n\nKills: " + str(playerskilled) + "\nDeaths: " + str(playerdeaths) + "\nKill/Death Ratio: " + str(killdeath) + "\n\n--- Firearms ---\n\nRounds Fired: " + str(shotstaken) + "\nBullets Hit: "+str(shotshit) + "\nAccuracy: " + str(accuracy) + "%\nHeadshots Hit: " + str(headshotshit) + "\nHeadshot Rate: " + str(headshotrate) + "%\n\n--- Zombies ---" + "\n\nZombies Killed: " + str(zombieskilled) + "\nMega Zombies Killed: " + str(megaskilled) + "\n\n--- Arena ---\n\nArena Wins: " + str(arenawins) + "```"
            await self.bot.say(msg)
        except:
            await self.bot.say("Looks like this user's profile is private, or they've never played Unturned before. Maybe they don\'t even exist! Enter a proper community ID or ID64 next time.")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 8, type=commands.BucketType.channel)
    async def steamid(self, ctx, steamid):
        """Convert from Vanity URL to ID64"""
        
        try:
            converted = steam.user.vanity_url('http://steamcommunity.com/id/' + steamid)
            steamname = steam.user.profile(str(converted)).persona
        except steam.user.VanityError:
            await self.bot.say('Vanity URL to ID64 conversion failed. User does not seem to exist.')
            return

        await self.bot.say('```Steam Vanity URL > Steam ID 64\n\nUser: {}\n\nVanity URL: {}\n\nSteam ID 64: {}```'.format(steamname, steamid, str(converted)))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 8, type=commands.BucketType.channel)
    async def osu(self, ctx, user):
        """Gives osu! statistics"""
        
        params = {'k' : self.osukey, 'u' : user}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://osu.ppy.sh/api/get_user', data=params) as resp:
                    data = await resp.json()
                    data = data[0]
                    
        except IndexError:
            await self.bot.say('The specified user (``{}``) was not found.'.format(user))
            return
        except Exception as e:
            await self.bot.say('``ERROR | {}``'.format(str(e)))
            return

        userid = data['user_id']
        username = data['username']
        playcount = data['playcount']
        totalscore = data['total_score']
        pprank = data['pp_rank']
        rawpp = data['pp_raw']
        accuracy = round(float(data['accuracy']), 2)
        country = data['country']
        rankcountry = data['pp_country_rank']

        embed = discord.Embed(title='osu! Standard Mode') \
                .set_author(name=username, icon_url='https://a.ppy.sh/{}'.format(userid)) \
                .set_thumbnail(url='https://a.ppy.sh/{}'.format(userid)) \
                .set_footer(text='Information retrieved from the osu! api. https://osu.ppy.sh/api/', icon_url='https://up.ppy.sh/files/osu!logo4-0.png') \
                .add_field(name='Username', value=username, inline=False) \
                .add_field(name='User ID', value=userid, inline=False) \
                .add_field(name='Rank', value='#{:,}'.format(int(pprank)), inline=False) \
                .add_field(name='Plays', value='{:,}'.format(int(playcount)), inline=False) \
                .add_field(name='Performance', value='{:,} pp'.format(round(float(rawpp)), 0), inline=False) \
                .add_field(name='Accuracy', value='{}%'.format(accuracy), inline=False) \
                .add_field(name='Total Score', value='{:,}'.format(int(totalscore)), inline=False) \
                .add_field(name='Country Rank', value='#{:,}'.format(int(rankcountry)), inline=False) \
                .add_field(name='Country', value=country, inline=False)
                
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, type=commands.BucketType.channel)
    async def query(self, ctx, server):
        """Queries an Unturned server"""
        if server == 'rekt':
            await self.bot.say('does not exist anymore, and is never coming back')
            return
        try:
            ip, port = server.split(':', 1)
        except ValueError:
            await self.bot.say('Correct format is ``x.x.x.x:12345``')
            return
        
        try:
            address = (ip, int(port))
        except:
            await self.bot.say('Invalid IP.')
            return
        
        server = valve.source.a2s.ServerQuerier(address, timeout=0.25)
        data = {}
        
        try:
            for i in server.info():
                data[i] = server.info()[i]
        except valve.source.a2s.NoResponseError:
            await self.bot.say('Timed out. Server is not online, or latency is too high.\n>Reminder that Unturned query ports are +1 over the connection port.')
            return
        except:
            await self.bot.say('Query failed. Please enter a valid IP.')
            return

        embed = discord.Embed(title=data['server_name']) \
                .add_field(name='Game', value=data['game'], inline=False) \
                .add_field(name='Ping', value=str(round(server.ping(), 2)) + 'ms', inline=False) \
                .add_field(name='Map', value=data['map'], inline=False) \
                .add_field(name='Players', value=str(data['player_count']) + '/' + str(data['max_players']), inline=False) \
                .add_field(name='Password', value='True' if data['password_protected'] == 1 else 'False', inline=False)

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 8, type=commands.BucketType.channel)
    async def unturnedprice(self, ctx, *, query):
        """Grabs price of unturned items from steam market"""
        
        data = await parse_item_data(query)
        
        if not data:
            if data is None:
                await self.bot.say('No items were found for ``{}``'.format(query))
                return
            if data is False:
                await self.bot.say('Error processing request. Try again later.'.format(query))
                return

        embed = discord.Embed(title=data['Name'], url='http://steamcommunity.com/market/listings/304930/{}'.format(data['url_enc'])) \
            .add_field(name='Price', value=data['Price'], inline=False) \
            .set_thumbnail(url=data['img_url']) \
            .set_footer(text='Prices retrieved from the Steam Community Market')


        await self.bot.say(embed=embed)
        

def setup(bot):
    bot.add_cog(games(bot))
