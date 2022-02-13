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
    async def sort_values(self, activities, uid):
        self.stat_channel = await self.bot.fetch_channel(self.creds["stat_channel"])
        user = await self.bot.fetch_user(uid)
        embed = discord.Embed(title = f"[CYCLE START] [{self.now()}]",
                                    url = "https://github.com/megumin00/league-uptime",
                                    description=f"caused by startup",
                                    color = 0xff0000)
        embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url = user.avatar_url)
        
        activity_typecases = {"<class 'discord.activity.Game'>" : "game_activity",
                              "<class 'discord.activity.CustomActivity'>" : "custom_activity",
                              "<class 'discord.activity.Spotify'>" : "spotify_activity",
                              "<class 'discord.activity.Activity'>" : "activity_activity"}

        return_dict = {uid: {}}
        
        for k, v in activity_typecases.items():
            #eg. k = "<class 'discord.activity.Game'>", v = "game_activity"
            for i in activities:
                if str(type(i)) == k:
                    #create embed rn
                    #send message so we can rereference later w/ message id
                    #if the current activity being added to field is spotify it will include additional info
                    if v == "spotify_activity":
                        embed.add_field(name=i, value=f"""None => {i.name}
Title: `{i.title}`
Artist: `{i.artist}`
ID: `{i.track_id}`""", inline = True)
                    else:
                        embed.add_field(name = v, value = f"None => {i.name}")

                    #send embed
                    message = await self.stat_channel.send(embed=embed)
                                         
                    nested_dict = {"time" : datetime.now,
                                   v : i,
                                   "mid" : str(message.id)}
                    return_dict[uid][v] = nested_dict

        return return_dict



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
                        filtered_user_activity = await self.sort_values(user.activities, member.id)
                        self.current_activities[member.id] = filtered_user_activity[member.id]

        #logging success
        await self.log_channel.send(f"""/// `[START] event-log` ///
[{self.now()}] [SUCCESS] Event cogs imported
[{self.now()}] [SUCCESS] User statuses logged...
```{self.current_activities}```
/// `[END] event-log` ///""")


    
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
            before_activities = await self.sort_values(before.activities, before.id)
            after_activities = await self.sort_values(after.activities, after.id)

            #check if old activity has ended
            

            #check if new activity has begun
            


        
    def now(self):
        now = datetime.now()
        dt_string = now.strftime("`%H:%M:%S` `%d/%m/%Y`")
        return dt_string



def setup(bot):
    bot.add_cog(on_member_update(bot))
