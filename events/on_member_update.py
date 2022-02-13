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
        
    def now(self):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
        return dt_string
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        self.ignore_bots = self.configs["ignore_bots"]
        if self.ignore_bots:
            user = await self.bot.fetch_user(after.id)
            if user.bot:
                return
            
        self.stat_channel = await self.bot.fetch_channel(int(self.creds["stat_channel"]))
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
                                        description=f"<@{uid}> | {old_activity} => {new_activity} | time elapsed: {time_spent}",
                                        color = 0x00ff00)

                    message = await self.stat_channel.fetch_message(mid)
                    await message.reply(embed=embed)
                    

            elif after.activity != None:
                embed=discord.Embed(title=f"[CYCLE START] [{self.now()}]",
                                        url="https://github.com/megumin00/league-uptime",
                                        description=f"<@{after.id}> | {before.activity} => {after.activity}",
                                        color = 0xff0000)
                sent = await self.stat_channel.send(embed=embed)
                self.activities[str(after.activity)] = {"uid" : after.id, "then" : datetime.now(), "mid" : sent.id}

def setup(bot):
    bot.add_cog(on_member_update(bot))
