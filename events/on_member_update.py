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


        
    @commands.command()
    async def sort_values(self, before_activities, after_activities, uid, cause):
        self.stat_channel = await self.bot.fetch_channel(self.creds["stat_channel"])
        user = await self.bot.fetch_user(uid)
        embed = discord.Embed(title = f"[CYCLE START] [{self.now()}]",
                                    url = "https://github.com/megumin00/league-uptime",
                                    description=f"caused by {cause}",
                                    color = 0xff0000)
        embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url = user.avatar_url)
        
        activity_typecases = {"<class 'discord.activity.Game'>" : "game_activity",
                              "<class 'discord.activity.CustomActivity'>" : "custom_activity",
                              "<class 'discord.activity.Spotify'>" : "spotify_activity",
                              "<class 'discord.activity.Activity'>" : "activity_activity"}

        return_dict = {uid: {}}
        
        for k, v in activity_typecases.items():
            #eg. k = "<class 'discord.activity.Game'>", v = "game_activity"
            for i in after_activities:
                if str(type(i)) == k:
                    #create embed rn
                    #send message so we can rereference later w/ message id
                    #if the current activity being added to field is spotify it will include additional info
                    
                    #if before_activities is equals to none (meaning this is caused by on_ready event)
                    if before_activities == None:
                        if v == "spotify_activity":
                            embed.add_field(name=i, value=f"""
None => {i.name}
Title: `{i.title}`
Artist: `{i.artist}`
ID: `{i.track_id}`""", inline = True)
                        else:
                            embed.add_field(name = v, value = f"None => {i.name}")
                    
                    #if before_activities has content in it
                    else:
                        #checks if keys are same, lesser or greater. (0 = same, 1 = before missing, 2 = after missing)
                        case = await self.find_equality(before_activities, after_activities, uid)
                        status_code = case["status_code"]
                        before_activities = case["before_dict"]
                        after_activities = case["after_dict"]
                        
                        for x in case["all_keys"]:
                            if x == "spotify_activity":
                                a = after_activities[x]
                                b = before_activities[x]
                                if a == None:
                                    a_title = None
                                    a_artist = None
                                    a_track_id = None
                                    
                                else:
                                    a_title = a.title
                                    a_artist = a.artist
                                    a_track_id = a.track_id
                                
                                if b == None:
                                    b_title = None
                                    b_artist = None
                                    b_track_id = None
                                
                                else:
                                    b_title = b.title
                                    b_artist = b.artist
                                    b_track_id = b.track_id
                                old_val = f"""
Title: `{b_title}`
Artist: `{b_artist}`
Track_ID: `{b_track_id}`
"""
                                
                                new_val = f"""
Title: `{a_title}`
Artist: `{a_artist}`
Track_ID: `{a_track_id}`
"""

                                embed.add_field(name = x+"_old", value=old_val, inline = True)
                                embed.add_field(name = x+"_new", value=new_val, inline = True)
                            else:
                                embed.add_field(name = f"{x}_old ", value = f"{before_activities[x]}")
                                embed.add_field(name = f"{x}_new ", value = f"{after_activities[x]}")
                            
                    #send embed
                    message = await self.stat_channel.send(embed=embed)
           
                        
                                         
                    nested_dict = {"time" : datetime.now,
                                   v : i,
                                   "mid" : str(message.id)}
                    return_dict[uid][v] = nested_dict

        return return_dict
    
    

    @commands.command()
    async def find_equality(self, user_before_activities, user_after_activities, uid):
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
            for b in user_before_activities:
                if str(type(b)) == k:
                    before_key_list.append(v)
                    before_dict[v] = b
                    
            for a in user_after_activities:
                if (str(type(a))) == k:
                    after_key_list.append(v)
                    after_dict[v] = a
        
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
                        filtered_user_activity = await self.sort_values(None, user.activities, member.id, "init")
                        self.current_activities[member.id] = filtered_user_activity[member.id]

        #logging success
        await self.log_channel.send(f"""/// `[START] event-log` ///
[{self.now()}] [SUCCESS] Event cogs imported
[{self.now()}] [SUCCESS] User statuses logged...""")

        count = 0
        send = ""
        for i in self.current_activities:
            user = await self.bot.fetch_user(i)
            await self.log_channel.send(f"[{self.now()}] ```[{user.name}#{user.discriminator}] {self.current_activities[i]}```")
        await self.log_channel.send("/// `[END] event-log` ///")


    
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
            #NOTE: before_activities is effectly current_acitivies
            before_activities = before.activities
            
            #print(self.current_activities)
            #print(before_activities==self.current_activities)
            after_activities = await self.sort_values(before_activities, after.activities, after.id, "event-detection")
            


        
    def now(self):
        now = datetime.now()
        dt_string = now.strftime("`%H:%M:%S` `%d/%m/%Y`")
        return dt_string



def setup(bot):
    bot.add_cog(on_member_update(bot))
