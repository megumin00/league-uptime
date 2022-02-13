import discord
import json
import asyncio

from datetime import datetime
from colorama import Fore, Back, Style
from discord.ext import tasks, commands

class main:
    def __init__(self):
        #loading data and config
        try:
            f = open("secret.json")
            self.creds = json.load(f)
            
        except:            
            dat = {
                "token" : "",
                "host" : "",
                "log_channel" : "",
                "stat_channel" : "",
            }
            
            with open("secret.json", "w") as jsonFile:
                json.dump(dat, jsonFile)

        try:
            f = open("config.json")
            self.config = json.load(f)

        except:            
                dat = {
                    "token" : "",
                    "host" : "",
                    "log_channel" : "",
                    "stat_channel" : "",
                }
                
                with open("config.json", "w") as jsonFile:
                    json.dump(dat, jsonFile)
        self.token = self.creds["token"]
        #load end
        
        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Streaming(name='with Foxes 🦊', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
            
            self.log_channel = await bot.fetch_channel(int(self.creds["log_channel"]))
            self.stat_channel = await bot.fetch_channel(int(self.creds["stat_channel"]))
            self.host = await bot.fetch_user(self.creds["host"])

            active = 'Bot has logged in as {0.user}'.format(bot)
            await self.log_channel.send(active)
            print(active)
            
            await self.log_channel.send(f"""
================
/// `[START] log` ///
[{self.now()}] [SUCCESS] Bot online.
[{self.now()}] [SUCCESS] Loading config.json...
[{self.now()}] config.json contents:.""")
            for i in self.config:
                await self.log_channel.send(f"[{self.now()}] `{i}` : `{self.config[i]}`")
            await self.log_channel.send(f"[{self.now()}] [END-LIST]")
            await self.log_channel.send("/// `[END] main-init-log` ///")
        
    def now(self):
        now = datetime.now()
        dt_string = now.strftime("`%H:%M:%S` `%d/%m/%Y`")
        return dt_string

    def load_cogs(self):
        bot.load_extension("cogs.main")
        bot.load_extension("events.on_member_update")

    def run(self):
        self.load_cogs()
        bot.run(self.token)

if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.remove_command('help')
    main = main()
    main.run()
