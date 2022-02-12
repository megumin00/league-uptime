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
            self.log_channel = await bot.fetch_channel(int(self.creds["log_channel"]))
            self.stat_channel = await bot.fetch_channel(int(self.creds["stat_channel"]))
            self.host = await bot.fetch_user(self.creds["host"])
            
            print('We have logged in as {0.user}'.format(bot))
            await self.log_channel.send(f"[{self.now()}] [SUCCESS] Bot online.")
            for i in self.config:
                

    def now(self):
        now = datetime.now()
        dt_string = now.strftime("`%H:%M:%S` `%d/%m/%Y`")
        return dt_string

    def load_cogs(self):
        bot.load_extension("cogs.main")

    def run(self):
        self.load_cogs()
        bot.run(self.token)

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='!')
    bot.remove_command('help')
    main = main()
    main.run()
