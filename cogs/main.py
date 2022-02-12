import discord
import datetime

from datetime import datetime
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.now = datetime.now()

    @commands.command()
    async def ping(self, message):
        await message.send("Pong!")

    @commands.command()
    async def uptime(self, message):
        days = datetime.now().day - self.now.day
        hours = datetime.now().hour - self.now.hour
        minutes = datetime.now().minute - self.now.minute
        seconds = datetime.now().second - self.now.second
        await message.send(f"""I have been online for:
`{days}` day(s), `{hours}` hour(s), `{minutes}` minute(s), `{seconds}` second(s)""")

def setup(bot):
    bot.add_cog(Main(bot))
