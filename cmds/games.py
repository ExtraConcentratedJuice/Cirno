from discord.ext import commands
import discord
import json
import requests
import random
import yaml
#lul xD api wrapper
import steam

class games():
    def __init__(self, bot):
        self.bot = bot

    with open("config.yaml", 'r') as f:
        config = yaml.load(f)
        
    steam.api.key.set(config['steamkey'])
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 6, type=commands.BucketType.user)
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
    async def steamid(self, ctx, steamid):
        """Convert from Vanity URL to ID64"""
        
        try:
            converted = steam.user.vanity_url('http://steamcommunity.com/id/' + steamid)
            steamname = steam.user.profile(str(converted)).persona
        except steam.user.VanityError:
            await self.bot.say('Vanity URL to ID64 conversion failed. User does not seem to exist.')
            return

        await self.bot.say('```Steam Vanity URL > Steam ID 64\n\nUser: {}\n\nVanity URL: {}\n\nSteam ID 64: {}```'.format(steamname, steamid, str(converted)))
def setup(bot):
    bot.add_cog(games(bot))
