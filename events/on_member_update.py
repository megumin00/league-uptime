import discord
import json
import asyncio

from datetime import datetime, time, timedelta
from discord.ext import commands

class on_member_update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        f = open("secret.json")
        a = open("config.json")
        
        self.creds = json.load(f)
        self.configs = json.load(a)
        
        self.ignore_bots = self.configs["ignore_bots"]

        self.current_activities = {}

    
    @asyncio.coroutine
    def find_equality(self, user_before_activities, user_after_activities, uid):
        #set typecases
        activity_typecases = {"<class 'discord.activity.Game'>" : "game_activity",
                              "<class 'discord.activity.CustomActivity'>" : "custom_activity",
                              "<class 'discord.activity.Spotify'>" : "spotify_activity",
                              "<class 'discord.activity.Activity'>" : "activity_activity"}
        
        #finding all key non-Nonetype key values and assigning to list
        before_key_list = []
        after_key_list = []
        all_keys = []
        
        before_dict = {}
        after_dict = {}
        
        for k, v in activity_typecases.items():
            if user_before_activities != None:
                for b in user_before_activities:
                    if str(type(b)) == k:
                        before_key_list.append(v)
                        before_dict[v] = b
            
            else:
                before_key_list = []
                 
            if user_after_activities != None:
                for a in user_after_activities:
                    if (str(type(a))) == k:
                        after_key_list.append(v)
                        after_dict[v] = a
            
            else:
                after_key_list = []
        
        return_value = {}
        #check if before_activites has key in after_activities 
        #case 1: all keys in before_activites are the same as after_activities
        if len(before_key_list) == len(after_key_list):
            return_value["status_code"] = 0
            all_keys = before_key_list
        
        #case 2: before_activities has a missing key in relation to after_activities
        elif len(before_key_list) < len(after_key_list):
            return_value["status_code"] = 1
            all_keys = after_key_list
            
            for i in before_key_list[:]:
                if i in after_key_list:
                    after_key_list.remove(i)
            
            for i in after_key_list:
                before_dict[i] = None
            
            
            
        #case 3: after_activities has a missing key in relation to before_activities
        else:
            return_value["status_code"] = 2
            all_keys = before_key_list
            
            for i in after_key_list[:]:
                if i in before_key_list:
                    before_key_list.remove(i)
            
            for i in before_key_list:
                after_dict[i] = None
        
        return_value["before_dict"] = before_dict
        return_value["after_dict"] = after_dict
        return_value["all_keys"] = all_keys
        
        return return_value
    
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = await self.bot.fetch_channel(self.creds["log_channel"])
        self.stat_channel = await self.bot.fetch_channel(self.creds["stat_channel"])
        self.ignore_bots = self.configs["ignore_bots"]
        
        #getting all members avaliable
        all_members = []
        for guild in self.bot.guilds:
            async for member in guild.fetch_members(limit=None):
                #ignoring bots if config for ignore_bot = True
                if self.ignore_bots and member.bot:
                    pass

                #getting all valid user activities
                elif member not in all_members:
                    user = guild.get_member(member.id)
                    if user.activity != None:
                        #assigning all current activities to self.current_activities
                        filtered_user_activity = await self.find_equality({}, user.activities, member.id)
                        status_code = filtered_user_activity["status_code"]
                        embed = await self.sort_case(status_code, filtered_user_activity, user.id)
                        
                        message_snowflake = await self.stat_channel.send(embed=embed)
                        #self.current_activities[member.id] = filtered_user_activity[member.id]
        
        '''
        #logging success
        await self.log_channel.send(f"""/// `[START] event-log` ///
[{self.now()}] [SUCCESS] Event cogs imported
[{self.now()}] [SUCCESS] User statuses logged...""")

        count = 0
        send = ""
        for i in self.current_activities:
            user = await self.bot.fetch_user(i)
            await self.log_channel.send(f"[{self.now()}] ```[{user.name}#{user.discriminator}] {self.current_activities[i]}```")
        await self.log_channel.send("/// `[END] event-log` ///")'''


    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):    
        current_guild = await self.bot.fetch_guild(after.guild.id)
        user = after.guild.get_member(after.id)

        cid = current_guild.id
        mgid = self.creds["main_guild"]

        #check if info is being taken from main_guild
        if str(cid) == mgid:
            return

        #ignores all bots if setting is toggled in config
        if self.ignore_bots and user.bot:
            return
        
        if before.activities != after.activities:
            embed = await self.activity_update(before, after)
            await self.stat_channel.send(embed=embed)


            
            
    def sort_spotify(self, case):
        #scuffed fix but it works :)
        if case["after_dict"]["spotify_activity"] != None:
            a_spotify_title = case["after_dict"]["spotify_activity"].title
            a_spotify_artist = case["after_dict"]["spotify_activity"].artist
            a_spotify_track_id = case["after_dict"]["spotify_activity"].track_id
        
        else:
            a_spotify_title = None
            a_spotify_artist = None
            a_spotify_track_id = None
            
        if case["before_dict"]["spotify_activity"] != None:
            b_spotify_title = case["before_dict"]["spotify_activity"].title
            b_spotify_artist = case["before_dict"]["spotify_activity"].artist
            b_spotify_track_id = case["before_dict"]["spotify_activity"].track_id
        
        else:
            b_spotify_title = None
            b_spotify_artist = None
            b_spotify_track_id = None
            
        old_val = f"""
Title: `{b_spotify_title}`
Artist: `{b_spotify_artist}`
Track_ID: `{b_spotify_track_id}`
"""
        new_val = f"""
Title: `{a_spotify_title}`
Artist: `{a_spotify_artist}`
Track_ID: `{a_spotify_track_id}`
"""
        
        return [old_val, new_val]
    
    
    @asyncio.coroutine
    async def activity_update(self, before, after):
            #NOTE: before_activities is effectly current_acitivies
            before_activities = before.activities
            after_activities = after.activities
            
            #print(self.current_activities)
            #print(before_activities==self.current_activities)
            case = await self.find_equality(before_activities, after_activities, after.id)
            status_code = case["status_code"]
            embed = await self.sort_case(status_code, case, after.id)
                        
            return embed  
        
        
    @asyncio.coroutine
    async def sort_case(self, status_code, case, uid):
        key_values = []
        embed = None
        user = await self.bot.fetch_user(uid)
        
        #get all current user activities
        for i in  case["before_dict"]:
            key_values.append(i)
            
        for key in key_values:
            #if activities are the same
            if status_code == 0:
                if embed == None:
                    embed = discord.Embed(title = f"[CYCLE CONTINUATION] [{self.now()}]",
                                          url = "https://github.com/megumin00/league-uptime",
                                          color = 0xff0000)
                    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url = user.avatar_url)
                
                if key == "spotify_activity":
                    val = self.sort_spotify(case)

                    embed.add_field(name = "spotify_old", value=val[0], inline = True)
                    embed.add_field(name = "spotify_new", value=val[1], inline = True)
                    
                else:
                    
                    embed.add_field(name = f"{key}_old", value=case["before_dict"][key], inline = True)
                    embed.add_field(name = f"{key}_new", value=case["after_dict"][key], inline = True)
                    
            #if before has more than after (start of cycle)
            elif status_code == 1:
                if embed == None:
                    embed = discord.Embed(title = f"[CYCLE INCREMENT] [{self.now()}]",
                                          url = "https://github.com/megumin00/league-uptime",
                                          color = 0xff0000)
                    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url = user.avatar_url)
                
                if key == "spotify_activity":
                    val = self.sort_spotify(case)

                    embed.add_field(name = "spotify_old", value=val[0], inline = True)
                    embed.add_field(name = "spotify_new", value=val[1], inline = True)
                    
                else:
                    
                    embed.add_field(name = f"{key}_old", value=case["before_dict"][key], inline = True)
                    embed.add_field(name = f"{key}_new", value=case["after_dict"][key], inline = True)
                #remove item from current_activites[uid]

            #if after has more than before (end of cycle)
            else:
                if embed == None:
                    embed = discord.Embed(title = f"[CYCLE END] [{self.now()}]",
                                          url = "https://github.com/megumin00/league-uptime",
                                          color = 0xff0000)
                    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url = user.avatar_url)
                
                if key == "spotify_activity":
                    val = self.sort_spotify(case)

                    embed.add_field(name = "spotify_old", value=val[0], inline = True)
                    embed.add_field(name = "spotify_new", value=val[1], inline = True)
                    
                else:
                    embed.add_field(name = f"{key}_old", value=case["before_dict"][key], inline = True)
                    embed.add_field(name = f"{key}_new", value=case["after_dict"][key], inline = True)
                    
        return embed
    
    
    def now(self):
        now = datetime.now()
        dt_string = now.strftime("`%H:%M:%S` `%d/%m/%Y`")
        return dt_string



def setup(bot):
    bot.add_cog(on_member_update(bot))
