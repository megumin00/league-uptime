import discord
import json
import asyncio

from datetime import datetime, time, timedelta
from discord.ext import commands

class on_member_update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activities = {}
        f = open("secret.json")
        self.creds = json.load(f)
        
        a = open("config.json")
        self.configs = json.load(a)

        self.current_activities = {}
        self.old_activities = {}
        
    def now(self):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
        return dt_string
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        self.ignore_bots = self.configs["ignore_bots"]
        self.stat_channel = await self.bot.fetch_channel(int(self.creds["stat_channel"]))
        
        

        current_guild = await self.bot.fetch_guild(after.guild.id)
        user = after.guild.get_member(after.id)

        cid = current_guild.id
        mgid = self.creds["main_guild"]

        if str(cid) == mgid:
            return
        
        if self.ignore_bots and user.bot:
            return

        if before.activities != after.activities:
            all_activities = {"<class 'discord.activity.CustomActivity'>" : "CustomActivity",
                              "<class 'discord.activity.Game'>" : "GameActivity",
                              "<class 'discord.activity.Spotify'>" : "SpotifyActivity",}
            old = before.activities
            new = after.activities

            uid = after.id
            
            #detects if current user activity is in current_activity
            if uid in self.current_activities:
                '''
                self.old_activities[uid] = self.current_activities[uid]
                self.current_activities[uid] = {}
                self.old_items = []
                self.missing_item = ""
                
                for key, value in all_activities.items():
                    for new_activity in new:
                        if str(new_activity.__class__) == key:
                            self.current_activities[uid][value] = new_activity
                
                #check what value is different from old_activities (ignoring mid)
                for i in self.current_activities[uid]:
                    self.old_items.append(i)

                for i in self.old_activities[uid]:
                    if i not in self.old_items and i != "mid":
                        self.missing_item = i

                print(self.old_activities[uid][self.missing_item])
                print(self.new_activites[uid][self.missing_item])
                #wipe values in
                '''
                pass
                    
                
            #if user is now active, status is added in current_activity
            elif after.activity != None: #change to filter properly
                #init embed
                embed=discord.Embed(title=f"[CYCLE START] [{self.now()}]",
                                        url="https://github.com/megumin00/league-uptime",
                                        description=f"<@{after.id}>",
                                        color = 0xff0000)
                
                #initialising dict (dict will clear)
                self.current_activities[uid] = {}
                self.old_activities[uid] = {}
                keys = []
                #activities: old & new
                
                #Base Activities:
                
                for key, value in all_activities.items():
                    for new_activity in new:
                        for i in keys:
                            old_activity[uid][i] = None
                            current_activities[uid][i] = None
                        
                        if str(new_activity.__class__) == key:
                            self.current_activities[uid][value] = new_activity

                            #initialising old_activity keys to be equal to new_activity keys, if there is value it will overwrite
                            keys.append(value)

                    
                        
                    for old_activity in old:
                        if str(self.old_activities.__class__) == key:
                            print(value, old_activity)
                            self.old_activities[uid][value] = old_activity

                        

                for i in self.current_activities[uid]:
                    if i == "SpotifyActivity":
                        embed.add_field(name=i, value=f"""{self.old_activities[uid][i]} => {self.current_activities[uid][i]}
Title: `{self.current_activities[uid][i].title}`
Artist: `{self.current_activities[uid][i].artist}`
ID: `{self.current_activities[uid][i].track_id}`""", inline = True)
                    else:
                        embed.add_field(name=i, value=f"{self.old_activities[uid][i]} => {self.current_activities[uid][i]}", inline = True)

                message = await self.stat_channel.send(embed=embed)
                try:
                    self.current_activities[uid]["mid"] = message.id
                except:
                    pass
                
                #clearing old activities to be reused
                self.old_activities = {}
        '''
        if before.activity != after.activity:
            if str(before.activity) in self.activities:
                if before.id == self.activities[str(before.activity)]["uid"]:
                    username = after.name
                    old_activity = before.activity
                    new_activity = after.activity
                    uid = self.activities[str(before.activity)]["uid"]
                    mid = self.activities[str(before.activity)]["mid"]
                    time_info = self.activities[str(before.activity)]["then"]
                    
                    time_spent = datetime.now() - time_info
                    if int(time_spent.total_seconds()) > 300:
                        time_spent = str(float(time_spent.total_seconds() / 60)) + "(m)"
                    else:
                        time_spent = str(int(time_spent.total_seconds())) + "(s)"

                    embed=discord.Embed(title="[CYCLE ENDED]",
                                        url="https://github.com/megumin00/league-uptime",
                                        description=f"<@{uid}>",
                                        color = 0x00ff00)

                    embed.add_field(name=f"Activity:", value = f"{before.activity} => {after.activity}")
                    try:
                        embed.add_field(name=f"Details: ", value=f"{before.activity.details} => {after.activity.details}")
                    except:
                        pass

                    embed.add_field(name="Time Elapsed: ", value = f"{time_spent}")
                    message = await self.stat_channel.fetch_message(mid)
                    await message.reply(embed=embed)
                    print(self.activities)
                    self.activities[str(before.activity)].pop(uid)
                    print(self.activities)

            elif after.activity != None:
                embed=discord.Embed(title=f"[CYCLE START] [{self.now()}]",
                                        url="https://github.com/megumin00/league-uptime",
                                        description=f"<@{after.id}>",
                                        color = 0xff0000)
                
                embed.add_field(name=f"Activity:", value = f"{before.activity} => {after.activity}")
                try:
                    embed.add_field(name=f"Details: ", value=f"{before.activity.details} => {after.activity.details}")
                except:
                    pass
                sent = await self.stat_channel.send(embed=embed)
                self.activities[str(after.activity)] = {"uid" : after.id, "then" : datetime.now(), "mid" : sent.id}
        '''
def setup(bot):
    bot.add_cog(on_member_update(bot))
