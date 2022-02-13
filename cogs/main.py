import discord
import json
import asyncio

from datetime import datetime
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startime = datetime.now()
        
        f = open("secret.json")
        self.creds = json.load(f)
        
        f = open("config.json")
        self.configs = json.load(f)
        
    def now(self):
        now = datetime.now()
        dt_string = str(now.strftime("`%H:%M:%S` `%d/%m/%Y`"))
        return dt_string
    
    @commands.command()
    async def ping(self, message):
        await message.send("Pong!")

    @commands.command()
    async def uptime(self, message):
        self.log_channel = await self.bot.fetch_channel(int(self.creds["log_channel"]))

        days = datetime.now().day - self.startime.day
        hours = datetime.now().hour - self.startime.hour
        minutes = datetime.now().minute - self.startime.minute
        seconds = datetime.now().second - self.startime.second
        await message.send(f"""I have been online for:
`{days}` day(s), `{hours}` hour(s), `{minutes}` minute(s), `{seconds}` second(s)""")

        await self.log_channel.send(f"[{self.now()}] [SUCCESS] <@{message.author.id}> used !uptime.")

    @commands.command()
    async def status(self, message):
        self.log_channel = await self.bot.fetch_channel(int(self.creds["log_channel"]))
        self.host = await self.bot.fetch_user(int(self.creds["host"]))
        self.ignore_bots = self.configs["ignore_bots"]
        
        if self.host.id != message.author.id:
            await self.log_channel.send(f"[{self.now()}] [FAIL] <@{message.author.id}> tried to used !status.")
            await message.send(f"[{self.now()}] [FAIL] <@{message.author.id}> tried to used !status. This incident has been recorded.")

        else:
            await self.log_channel.send(f"[{self.now()}] [SUCCESS] <@{message.author.id}> used !status.")
            currently_active = {}
            
            for guilditem in self.bot.guilds:
                await message.channel.send(f"Guild: {guilditem}")
                
                included_users = []
                field_len = 0
                longest_len = 0
                part = 1
                self.embed = discord.Embed(title = f" /// Guild {guilditem} /// (2000 character limit)",
                                                   url = "https://github.com/megumin00/league-uptime",
                                                   color = 0x87cefa)
                self.embed.set_author(name="powered by kemo",
                                      url="https://github.com/megumin00/league-uptime",
                                      icon_url="https://cdn.discordapp.com/attachments/929639388168745011/942105374675333141/FIREFOX.jpg")
                self.embed.set_footer(text="Powered with 💜 by Suwa")
                
                async for member in guilditem.fetch_members(limit=None):
                    if len(member.name) > longest_len:
                        longest_len = (len(member.name))

                async for member in guilditem.fetch_members(limit=None):
                    member_eq = f"{member.name}"
                    member_eq += " " * (longest_len - len(member.name))
                    activ = guilditem.get_member(member.id).activity
                    
                    if activ != None:
                        if self.ignore_bots and member.bot:
                            pass
                        else:
                            currently_active[member_eq] = activ.name
                            activ = f"**{activ.name}**"
                        
                    field_len += 1
                    if member.id not in included_users:
                        if self.ignore_bots and member.bot:
                            pass
                        else:
                            self.embed.add_field(name = "User: ", value = f"<@{member.id}>\n id: {member.id}\n activity: {activ}\n")
                            included_users.append(member.id)

                    if field_len >= 32 :
                        await message.send(embed=self.embed)
                        for i in range(1, 32):
                            self.embed.remove_field(index=i)
                        field_len = 0
                        
                    
                await message.send(embed=self.embed)
            full_list = """"""
            
            for i in currently_active:
                if "league of legend" in str(currently_active[i]):
                    full_list += f"`{i} is playing:   {currently_active[i]} 🚨 LEAGUE OF LEGENDS DETECTED 🚨`\n"
                else:
                    full_list += f"`{i} is playing:   {currently_active[i]}`\n"
                                    
            await message.send(f"""ALL CURRENTLY ACTIVE: `ignore_bots = {self.ignore_bots}`
{full_list}""")

            await self.log_channel.send(f"[{self.now()}] [SUCCESS] <@{message.author.id}>'s status activity has returned: \n{full_list}")

    @commands.command(aliases=['poweroff', 'shutdown'])
    async def quit(self, message):
        self.log_channel = await self.bot.fetch_channel(int(self.creds["log_channel"]))
        self.host = await self.bot.fetch_user(int(self.creds["host"]))
        if self.host.id != message.author.id:
            await self.log_channel.send(f"[{self.now()}] [FAIL] <@{message.author.id}> tried to used !poweroff.")
            await message.send(f"[{self.now()}] [FAIL] <@{message.author.id}> tried to used !poweroff. This incident has been recorded.")
        else:
            await message.send(f"[{self.now()}] [SUCCESS] <@{message.author.id}> used !poweroff. Disabling bot now.")
            await self.log_channel.send(f"[{self.now()}] [SUCCESS] <@{message.author.id}> has used !poweroff. Disabling bot now.")
            await self.log_channel.send("/// end-of-log ///")
            quit()

def setup(bot):
    bot.add_cog(Main(bot))
