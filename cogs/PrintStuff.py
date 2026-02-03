import os

import discord
import mcstatus
from discord import app_commands
from discord.ext import commands, tasks
from typing import Optional, Literal
import random
import asyncio
import string
import json
import re

from discord.ui import View, Button

global stopp
import datetime
from PIL import Image

stopp = False
bluff = False

class PrintStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task.start()

    async def printto(self, m: str):
        print(m)
        channel = await self.bot.fetch_channel(1434085176320852018)
        if channel is None:
            channel = await self.bot.get_channel(1434085176320852018)

        try:
            if len(str(m)) > 2000:
                n = []
                i = 0
                for i in range(0, len(m), 1900):
                    await channel.send(m[i:i + 1900])
            else:
                await channel.send(m)
        except Exception as error:
            print(str(error))
            print(error)
            try:
                await channel.send(str(error))
                await channel.send(error)
            except Exception as error:
                print("ok that's enough try catch")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.printto("Print Stuff online")

    #-----------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):


        #---------------------------------------notices your non anon------------------------------------------#
        if message.channel.id == 841490511390048277 and message.author.id != self.bot.user.id:
            cnt = message.content
            ch = message.channel
            if message.attachments:
                files = [await attachment.to_file() for attachment in message.attachments]
                await ch.send(files=files)
            await message.delete()
            cnt = await self.oddyspeak(cnt)
            await ch.send(cnt)

        #----------------------------------------killing x image sender----------------------------------------#
        if "killing" in message.content.lower():
            await self.catimg(message)

        usettings = self.bot.get_cog("SetStuff")

        # Ignore messages from the bot itself to prevent infinite loops (and sends anons to dmlink)
        if message.author == self.bot.user:
            if message.channel.id == 841490511390048277:
                people = await usettings.get_people()
                for person in people:
                    person = await self.bot.fetch_user(int(person))
                    await person.send(message.content)
            return

        #send dms to anon chat
        if isinstance(message.channel, discord.DMChannel) and message.author.id != self.bot.user.id:
            if await usettings.get_falsey_value(message, message.author, "dmtochat"):
                anon = await self.bot.fetch_channel(841490511390048277)
                await anon.send(await self.oddyspeak(message.content))
                if message.attachments:
                    files = [await attachment.to_file() for attachment in message.attachments]
                    await anon.send(files = files)


        #Teto of the day for today
        if random.random() < 0.5 and "today" in message.content.lower() and await usettings.get_value(message, message.author, "tetoday"):
            await self.kasane(message)
        #Remove identifiers from youtube links & fandom
        if "https://" in message.content and "?si=" in message.content:
            time = ""
            if "&t=" in message.content:
                time = message.content[message.content.index("&t="):]
                if " " in time:
                    time = time[:time.index(" ")]
                if "\n" in time:
                    time = time[:time.index(" ")]
                print(f"length: {len(time)}, string: {time}")
            bettermessage = message.content[:message.content.index("?si=")]
            print(bettermessage)
            print(bettermessage.index("https://"))
            bettermessage = bettermessage[bettermessage.index("https://"):]
            bettermessage = bettermessage + time
            await message.reply("oi I don't wanna get TRACKED. Click this instead, it won't give you a virus :D\n" + bettermessage, mention_author=False)
        if "https://" in message.content and "fandom" in message.content and "anti" not in message.content:
            bettermessage = message.content[message.content.index("https://"):]
            bettermessage = bettermessage.replace("fandom", "antifandom")
            if " " in bettermessage:
                bettermessage = bettermessage[:bettermessage.index(" ")]
            if "\n" in bettermessage:
                bettermessage = bettermessage[:bettermessage.index(" ")]
            await message.reply("ewwwwwwwwwwww FANDOM? in THIS economy??? nah go here instead.\n" + bettermessage)
        # -------------------------------------wordle e bot collab------------------------------------------#
        if message.author.id == 1211781489931452447 and ("X/6" in message.content or "6/6" in message.content):
            wmess = message

            global currlist

            if wmess.author.id == 1211781489931452447 and "Here are yesterday's results:" in wmess.content:
                words = ""
                exlist = []
                sixlist = []

                if "X/6" in wmess.content:
                    words = wmess.content[wmess.content.index("X/6:"):]
                if "6/6" in wmess.content:
                    words = wmess.content[wmess.content.index("6/6:"):]
                words = words.replace("\n", " ")
                words = words.split(" ")

                await self.printto(words)

                for g in words:
                    await self.printto(g)
                    if "<@" in g and len(g) > 10:
                        wid = int(g[2:len(g) - 1])
                        await self.printto(wid)

                        peep = await self.bot.fetch_user(wid)
                        await self.printto(peep)
                        currlist.append(peep)
                    elif "X/6" in g:
                        await self.printto("use da failures list")
                        currlist = exlist
                    elif "6/6" in g:
                        await self.printto("use almost failures list")
                        currlist = sixlist
                    else:
                        await self.printto("frick is that, that ain't an ID")
                await self.printto("6/6: ", sixlist)
                await self.printto("X/6: ", exlist)
                for guy in exlist:
                    await guy.send("bro failed the wordle smh my head emoji skill issue")
                for guy in sixlist:
                    await guy.send("got the wordle on the last try, not even close")

        # -------------------------------------responds to bluff------------------------------------------#
        global bluff
        if bluff and "e, " in message.content and "bluff" not in message.content:
            await message.reply("o7 on it", mention_author=False)
            bluff = False
        #---------------------------------------door stuff print stuff collab-----------------------------------#
        if message.channel.id == 1461631744955514932:
            channelrole = message.author.guild.get_role(1462230075503149299)
            if channelrole not in message.author.roles:
                await message.author.send("you should GAMBLE WITH DOORS\neven normal doors will give time")
                await message.delete()


    #----------------------------reincarnated as a helper command :D----------------------------------------#
    async def oddyspeak(self, message: str) -> string:
        mess = message.lower()
        result = message
        result = result[0].lower() + result[1:]
        try:
            if "ington" in mess:
                result = result.replace("ington", "")
            if "josh" in mess:
                result = re.sub("josh", "Josh <:crazy:1178765587929890877>", result, flags=re.IGNORECASE)
            if "mariofan" in mess:
                result = re.sub("mariofan", "Mariofan <:mewrlefan:1399225627655147550>", result, flags=re.IGNORECASE)
            elif "mario" in mess and "fan" not in mess:
                result = re.sub("mario", "Mariofan <:mewrlefan:1399225627655147550>", result, flags=re.IGNORECASE)
            if "edwosk" in mess:
                result = re.sub("edwosk", "Edwosk <:riskwosk:1363696488068153445>", result, flags=re.IGNORECASE)
            if "astro" in mess:
                result = re.sub("astro", "Astro <:green_sus:786757714121457664>", result, flags=re.IGNORECASE)
                if "naut" in mess:
                    mess.replace("naut", "")
            if "cb" in mess:
                result = re.sub("cb", "CB <:SmugPac:833531321061343232>", result, flags=re.IGNORECASE)
            if "omar" in mess:
                result = re.sub("omar", "Omar <:welp:1363696460343804004>", result, flags=re.IGNORECASE)
            if "rover" in mess:
                result = re.sub("rover", "Rover <:Maxwell_I_Guess:1400716442697072651>", result, flags=re.IGNORECASE)
            elif "rov" in mess:
                result = re.sub("rov", "Rover <:Maxwell_I_Guess:1400716442697072651>", result, flags=re.IGNORECASE)
            if "anth" in mess:
                result = re.sub("anth", "Anth <:anth:1363704263402061985>", result, flags=re.IGNORECASE)
            return result
        except Exception as e:
            print(e)
            print(str(e))
            return "e"



    # ------------------------------------------Bluff----------------------------------------------------------#
    @commands.hybrid_command(name="bluff", brief = "Tell e bot to do something, even if it can't.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def fakeit(self, ctx):
        global bluff
        bluff = True
        await ctx.send(content = "o7", ephemeral = True)
        await ctx.bot.process_commands(ctx)
    # ----------------------------------Date since made--------------------------------------------#
    @commands.hybrid_group(brief="created")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def time(self, ctx):
        await self.printto("obsolete")
        await self.bot.process_commands(ctx)
    @time.command()
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def created(self, ctx):
        await ctx.send(f"<t:{1748565600}:R>")
        await self.bot.process_commands(ctx)

    @commands.hybrid_command()
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def oddesay(self, ctx, words):
        anon = await self.bot.fetch_channel(841490511390048277)
        words = await self.oddyspeak(words)
        await anon.send(words)
        nerd = await ctx.send("e", ephemeral = True)
        await nerd.delete()

    #--------------------------------------Ping omar-----------------------------------------------#
    @commands.hybrid_command(name = "omarhelpweneedyougeton")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def omarhelpweneedyougeton(self, ctx):
        response = await ctx.send("Get someone else to press this button")
        async def pingomar(interaction: discord.Interaction):
            if interaction.user.id == ctx.author.id:
                await interaction.response.edit_message(content="get someone ELSE to press it.")
                return
            omuh = await self.bot.fetch_user(1120130858779689032)
            await omuh.send("e")
            await interaction.response.edit_message(content = "o7 he's *aware* now", view = None)
        buttonholder = View(timeout=120)
        helpbutton = Button(label="Ping Omar", style=discord.ButtonStyle.green)
        helpbutton.callback = pingomar
        buttonholder.add_item(helpbutton)
        await response.edit(view = buttonholder)

    #--------------------------------------Roll the dice-----------------------------------------#
    @commands.hybrid_command(name = "roll")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def roll(self, ctx, upper_bound: int, lower_bound: int = 1):
        try:
            if upper_bound < lower_bound:
                await ctx.send("If the upper bound is below 1, you gotta set the lower one too ._.")
                return
            elif lower_bound == upper_bound:
                await ctx.send(f"rolled {lower_bound}\n(What a hard choice THAT was.)")
                return
            await ctx.send(f"rolled {random.randint(lower_bound, upper_bound)}")
        except Exception as e:
            print(e)

    #-------------------------------Reports mc server status & players when requested--------------------------------#
    @commands.hybrid_group(name = "server", brief = "up\n role add | remove")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def server(self, ctx):
        await self.printto("obsolete")
    @server.command(name = "up")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def up(self, ctx):
        usettings = self.bot.get_cog("SetStuff")
        sessage = await ctx.send("uh")
        try:
            server = mcstatus.JavaServer.lookup("true-cigarette.gl.joinmc.link")
            st = server.status()
            await self.printto(st.players.online)
            count = st.players.online
            if random.random() < 1/90 and await usettings.get_value(ctx, ctx.author, "serverlie"):
                sessage = await sessage.channel.fetch_message(sessage.id)
                await sessage.edit(content="Nope...")
                return
            else:
                sessage = await sessage.channel.fetch_message(sessage.id)
                await sessage.edit(content = f"yea, {f"{count} guys on." if count > 1 else "1 guy on." if count == 1 else "but nobody's on ._."}")
            try:
                dudes = st.players.sample
                dudelist = ""
                if len(dudes) > 1:
                    for dude in dudes:
                        dudelist = dudelist + dude.name + ", "
                elif len(dudes) == 1:
                    dudelist = dudes[0].name
                if len(dudes) >=1:
                    await ctx.send(f"{dudelist}.")

            except Exception as error:
                await self.printto(str(error))
                await self.printto("error handling for error that made empty server = offline server bc error handling is funny")
        except BrokenPipeError as e:
            sessage = await sessage.channel.fetch_message(sessage.id)
            await sessage.edit(content = "idk it failed in a weird way do it again")
        except Exception as e:
            await self.printto("error: " + str(e))
            if random.random() < 1/90 and await usettings.get_value(ctx, ctx.author, "serverlie"):
                sessage = await sessage.channel.fetch_message(sessage.id)
                await sessage.edit(content="Yeah One guy one there")
                await sessage.channel.send("Mariofan527")

            else:
                sessage = await sessage.channel.fetch_message(sessage.id)
                await sessage.edit(content = f"nah")

    @up.error
    async def mcstatus_error(self, ctx, error):
        await self.printto(f"trying, but {error}")
        await ctx.channel.send("idk something broke")

    #helper command for checking if server is up in main, exists to avoid importing mcstatus *again* in main
    # async def sup(self):
    #     try:
    #         server = mcstatus.JavaServer.lookup("true-cigarette.gl.joinmc.link")
    #         server.status().players.online
    #         await self.printto("Server online")
    #         return 1
    #     except BrokenPipeError as e:
    #         await self.printto("weird error with sup, " + str(e) + "\n time to try again :D\n(This used to cause false negatives)")
    #         return await self.sup()
    #     except Exception as e:
    #         await self.printto(str(e))
    #         await self.printto(e)
    #         await self.printto("Server offline")
    #         return 0
    # #------------------------------------Server role management---------------------------------------------#
    # @server.group(name = "role")
    # async def role(self, ctx):
    #     await self.printto("obsolete")
    #
    # @role.command(name = "add")
    # async def role_add(self, ctx):
    #     await ctx.author.add_roles(ctx.author.guild.get_role(1426289745784340591))
    #     await ctx.send("o7 you're in")
    #
    # @role.command(name = "remove")
    # async def role_remove(self, ctx):
    #     await ctx.author.remove_roles(ctx.author.guild.get_role(1426289745784340591))
    #     await ctx.send("o7 it's gone")
    #


    #----------------------------------------Hit singer Kasane Teto----------------------------------------------------#

    @commands.hybrid_group(name = "daily", breif = "teto")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def daily(self, ctx):
        await self.printto("obsolete")
    @daily.command(name="teto", brief = "posts the day's teto")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def kasane(self, ctx):
        usettings = self.bot.get_cog("SetStuff")
        tetos = ["https://tenor.com/view/kasane-gif-10240710281900746822",
                 "https://tenor.com/view/teto-kasane-teto-teto-tuesday-utauloid-gif-25302042",
                 "https://tenor.com/view/kasane-gif-17215851662996724170",
                 "https://tenor.com/view/kasane-gif-5116923922296405686",
                 "https://tenor.com/view/kasane-gif-15454379637737486111",
                 "https://tenor.com/view/kasane-gif-5126225881107011559",
                 "https://tenor.com/view/kasane-gif-17280510370772186668",
                 "https://tenor.com/view/miku-hatsune-miku-anime-dance-silly-gif-7439677361449276795"]
        try:
            if random.random() < 1/20 and await usettings.get_value(ctx, ctx.author, "tetnot"):
                await self.printto("wait that's not teto")
                await ctx.reply(tetos[7], mention_author=False)
            else:
                await self.printto("teto")
                await ctx.reply(tetos[datetime.date.today().weekday()], mention_author=False)
        except Exception as e:
            await self.printto(e)
            await self.printto(str(e))
    @tasks.loop(seconds=1)
    async def aintnoway(self):
        lotto = random.random()

        if lotto < 0.00000000001:
            await self.printto(f"AIN'T NO WAAAAAYYYYYYYYY we hit the billion chance with {lotto}") #Console server
            thatonemf = await self.bot.fetch_user(405197452833062912)
            await thatonemf.send("Don't forget the heart patch")
            chat = await self.bot.get_channel(773015468201345027)
            await chat.send("@everyone BUY A FRICKIN LOTTERY TICKET RIGHT NOW,\n and also don't forget the heart patch <:fennyalove:1466317750732455978>")
        elif lotto < 0.000001:
            await self.printto(f"{lotto} isn't quite 1 in a billion, but still kinda neat .-.")

    #-----------------------------------Anim progress tracker-----------------------------------------#
    @tasks.loop(minutes=120)
    async def task(self):
        try:
            channel = self.bot.get_channel(1282010600322629652)

            if channel is None:
                await self.printto("channel was none, trying with fetch")
                channel = await self.bot.fetch_channel(1282010600322629652)

            if datetime.datetime.now().hour == 0 or datetime.datetime.now().hour == 23:
                day = -1
                try:
                    with open("updayt.txt", 'r') as f:
                        line = f.readline()
                        day = int(line.strip())  # Strip whitespace and convert to int
                except FileNotFoundError:
                    with open("updayt.txt", "x") as f:
                        f.write("2")
                        day= 2
                        await self.printto("made a file since it wasn't there, running as if was offline")

                day -= 1
                match day:
                    # case 3:
                    #     await channel.send("3 days left :D")
                    case 2:
                        await channel.send("2 days left :)")
                        await channel.send(file=discord.File("timesatickin.png"))

                    case 1:
                        await channel.send("https://tenor.com/view/majoras-mask-majora-zelda-final-day-gif-26658556")
                    case 0:
                        await channel.send("oopsie? I guess I've either accepted my fate or I'm speedrunning.")
                    case x if x > 5:
                        await self.printto("eh")
                    case _:
                        await channel.send(f"I don't know what I am doing. {day} days left, this message shouldn't be possible to see and only exists for error handling. \n PLEASE tell me I didn't go negative in days remaining")

                with open("updayt.txt", "w") as f:
                    f.write(f"{day}")
        except Exception as e:
            await self.printto(e)
            await self.printto(str(e))

    #--------------------------------Check anim days left----------------------------------------------#
    @commands.hybrid_group(name = "animation", brief = "time reset\n due in\n favors owed\ndays reserved")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def animation(self, ctx):
        await self.printto("obsolete")
    @commands.group(name = "dev", hidden = True)
    async def dev(self, ctx):
        print("obsolete")
    @dev.command(name = "set", hidden = True)
    async def set(self, ctx, days: int):

        if "dev" in ctx.author.nick:
            with open("updayt.txt", 'r+') as f:
                prev = f.readline()
                f.seek(0)
                f.truncate()
                f.write(str(days))
                await ctx.send(f"changed {prev} days to {days}")
    @animation.group(name = "due", brief = "in")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def due(self, ctx):
        await self.printto("obsolete")
    @due.command(name = "in")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def within(self, ctx):
        day = -1
        try:
            with open("updayt.txt", 'r') as f:
                line = f.readline()
                day = int(line.strip())  # Strip whitespace and convert to int
        except FileNotFoundError:
            with open("updayt.txt", "x") as f:
                f.write("2")
                day = 2
                await self.printto("made a file since it wasn't there, running as if was offline")
        match day:
            case 4:
                await ctx.send("4 days left technically, made progress today .-.")
            case 3:
                await ctx.send(f"3 days :D")
            case 2:
                await ctx.send(f"2 days")
                await ctx.send(file=discord.File("timesatickin.png"))
            case 1:
                await ctx.send(f"TODAY.")
                await ctx.send("https://tenor.com/view/majoras-mask-majora-zelda-final-day-gif-26658556")
            case _:
                await ctx.send(f"like {day}, he done messed up now. what a nerd")

    @animation.group(name = "time", brief = "reset")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def tiempo(self, ctx):
        await self.printto("obsolete")
    @tiempo.command(name = "reset")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def reset(self, ctx):
        if not (ctx.author.id == 702906770003198003 or ctx.author.id == 405197452833062912):
            await ctx.send("Imma don't think you're allowed to do dat")
            await ctx.send("https://tenor.com/view/luigi-coo-coo-crazy-luigis-mansion-dark-moon-gif-1213275346224547321")
            return
        with open("updayt.txt", "w") as f:
            f.write(f"4")
        await ctx.send("https://tenor.com/view/majoras-mask-zelda-songoftime-ocarina-gif-22880234")
        await asyncio.sleep(12)
        async for message in ctx.channel.history(limit=6):  # Adjust limit as needed
            if message.author == self.bot.user:
                await message.delete()
                break
        await ctx.send("o7 he gets time... *for now*...")

#--------------------------------------------Favor tracking---------------------------------------------
    @animation.group(name = "favors")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def favor(self, ctx):
        await self.printto("obsolete")
    @favor.command(name = "add")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def favadd(self, ctx, number: int):
        if not (ctx.author.id == 702906770003198003 or ctx.author.id == 405197452833062912):
            await ctx.send("Imma don't think you're allowed to do dat")
            await ctx.send("https://tenor.com/view/luigi-coo-coo-crazy-luigis-mansion-dark-moon-gif-1213275346224547321")
            return
        curr = 0
        try:
            with open("favors.txt", 'r') as f:
                curr = int(f.readline().strip())
        except FileNotFoundError:
            with open("favors.txt", "x") as f:
                f.write("0")
        with open("favors.txt", "w") as f:
            f.write(f"{curr + number}")
        await ctx.send(f"o7 added {number}")

    @favor.command(name = "owed")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def favowed(self, ctx):
        favors = 0
        try:
            with open("favors.txt", 'r') as f:
                favors = int(f.readline().strip())
        except FileNotFoundError:
            with open("favors.txt", "x") as f:
                f.write("0")
        await ctx.send(f"{favors} favors owed\n ._.")

    # --------------------------------------------reserve tracking---------------------------------------------
    @animation.group(name="reserves")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def reserve(self, ctx):
        await self.printto("obsolete")

    @reserve.command(name="add")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def resadd(self, ctx, number: int):
        if not (ctx.author.id == 702906770003198003 or ctx.author.id == 405197452833062912):
            await ctx.send("Imma don't think you're allowed to do dat")
            await ctx.send(
                "https://tenor.com/view/luigi-coo-coo-crazy-luigis-mansion-dark-moon-gif-1213275346224547321")
            return
        curr = 0
        try:
            with open("reserve.txt", 'r') as f:
                curr = int(f.readline().strip())
        except FileNotFoundError:
            with open("reserve.txt", "x") as f:
                f.write("0")
        with open("reserve.txt", "w") as f:
            f.write(f"{curr + number}")
        await ctx.send(f"o7 added {number}")

    @reserve.command(name="stored")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def resget(self, ctx):
        reserve = 0
        try:
            with open("reserve.txt", 'r') as f:
                reserve = int(f.readline().strip())
        except FileNotFoundError:
            with open("reserve.txt", "x") as f:
                f.write("0")
        await ctx.send(f"{reserve} days reserved\n \\_._")

    # ----------------------------------Deltarune tomorrow--------------------------------------------#
    @commands.hybrid_group(name="deltarune", brief="tomorrow")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def deltarune(self, ctx):
        await self.printto("obsolete")
        await self.bot.process_commands(ctx)
    @deltarune.command(name="tomorrow", brief="deltarune tomorrow")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def tomorrow(self, ctx):
        await ctx.reply("Deltarune tomorrow", mention_author=False)
        await self.bot.process_commands(ctx)

    #---------------------------------KILL IT WITH FIRE--------------------------------------------------#
    @commands.hybrid_group()
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def killit(self, ctx):
        await self.printto("obsolete")
    @killit.group(name = "with")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def using(self, ctx):
        await self.printto("obsolete")
    @using.command(name = "fire")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def fire(self, ctx):
        if ctx.message.reference:
            replied_message_id = ctx.message.reference.message_id
            try:
                replied_message = await ctx.channel.fetch_message(replied_message_id)
                if replied_message.author == self.bot.user:
                    await ctx.send("It's gone, we're safe now.\n YOU ALL SAW NOTHING", ephemeral=True)
                    await replied_message.delete()
                else:
                    await ctx.send("uh... that's not one of mine, that's your problem.\n Ask them really, REALLY, **REALLY** nicely to delete it, I'm sure that'll go well.")
            except discord.NotFound:
                await ctx.send("That, uh... doesn't exist anymore?")
        else:
            async for m in ctx.channel.history(limit=30):
                if m.author == self.bot.user:
                    await m.delete()
                    await ctx.send("o7 found it", ephemeral=True)
                    return

    # ----------------------------------:__: sender---------------------------------------------3
    @commands.hybrid_command(name = "o__o")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def dread(self, ctx):
        await ctx.reply("<:o__o:1429555147238805684>")
    # ----------------------------------Quote series--------------------------------------------#
    @commands.hybrid_group(brief = "from | random")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def quote(self, ctx):
        await self.printto("obsolete")
    #quote helper command
    def loadjson(self, value) -> list:
        global ql
        match value:
            case 0:
                with open("quotes/anth.json", "r") as file:
                    ql = json.load(file)
            case 1:
                with open("quotes/astro.json", "r") as file:
                    ql = json.load(file)
            case 2:
                with open("quotes/cb.json", "r") as file:
                    ql = json.load(file)
            case 3:
                with open("quotes/edwosk.json", "r") as file:
                    ql = json.load(file)
            case 4:
                with open("quotes/josh.json", "r") as file:
                    ql = json.load(file)
            case 5:
                with open("quotes/mariofan.json", "r") as file:
                    ql = json.load(file)
            case 6:
                with open("quotes/meowsor.json", "r") as file:
                    ql = json.load(file)
            case 7:
                with open("quotes/omar.json", "r") as file:
                    ql = json.load(file)
            case 8:
                with open("quotes/other.json", "r") as file:
                    ql = json.load(file)
            case 9:
                with open("quotes/otter.json", "r") as file:
                    ql = json.load(file)
            case 10:
                with open("quotes/rover.json", "r") as file:
                    ql = json.load(file)
        return ql

    @quote.command(name="random")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def randomQ(self, ctx, ephem=False):
        rand = random.randint(0, 16 + 274 + 212 + 42 + 103 + 264 + 125 + 122 + 54 + 6 + 25 - 1)
        choice = 8
        match rand:
            case c if 0 <= c <= 16:
                choice = 0
            case c if 16 <= c <= 16 + 248:
                choice = 1
            case c if 16 + 248 <= c <= 16 + 248 + 209:
                choice = 2
            case c if 16 + 248 + 209 <= c <= 16 + 248 + 209 + 52:
                choice = 3
            case c if 16 + 248 + 209 + 52 <= c <= 16 + 248 + 209 + 52 + 83:
                choice = 4
            case c if 16 + 248 + 209 + 52 + 83 <= c <= 16 + 248 + 209 + 52 + 83 + 228:
                choice = 5
            case c if 16 + 248 + 209 + 52 + 83 + 228 <= c <= 16 + 248 + 209 + 52 + 83 + 228 + 136:
                choice = 6
            case c if 16 + 248 + 209 + 52 + 83 + 228 + 136 <= c <= 16 + 248 + 209 + 52 + 83 + 228 + 136 + 124:
                choice = 7
            case c if 16 + 248 + 209 + 52 + 83 + 228 + 136 + 124 <= c <= 16 + 248 + 209 + 52 + 83 + 228 + 136 + 124 + 97:
                choice = 8
            case c if 16 + 248 + 209 + 52 + 83 + 228 + 136 + 124 + 97 <= c <= 16 + 248 + 209 + 52 + 83 + 228 + 136 + 124 + 97 + 6:
                choice = 9
            case c if 16 + 248 + 209 + 52 + 83 + 228 + 136 + 124 + 97 + 6 <= c <= 16 + 248 + 209 + 52 + 83 + 228 + 136 + 124 + 97 + 6 + 21:
                choice = 10

        quotelist = self.loadjson(choice)

        await ctx.send(quotelist[random.randint(0, len(quotelist) - 1)], ephemeral=ephem)

    @quote.command(name="from")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def fromQ(self, ctx, guy: Literal["Anth", "Astro", "CB", "Edwosk", "Josh", "Mariofan", "Meowsor", "Omar", "Otter", "Rover", "Other"], ephem=False):
        try:
            pulled = 8
            match guy:
                case "Anth":
                    pulled = 0
                case "Astro":
                    pulled = 1
                case "CB":
                    pulled = 2
                case "Edwosk":
                    pulled = 3
                case "Josh":
                    pulled = 4
                case "Mariofan":
                    pulled = 5
                case "Meowsor":
                    pulled = 6
                case "Omar":
                    pulled = 7
                case "Other":
                    await self.printto("idk")
                    pulled = 8
                case "Otter":
                    pulled = 9
                case "Rover":
                    pulled = 10

            quotelist = self.loadjson(pulled)
            await ctx.send(quotelist[random.randint(0, len(quotelist) - 1)], ephemeral=ephem)
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)
            await self.printto(str(error))

    async def catimg(self, message: discord.Message):
        content = message.content
        quotee = message.content[message.content.lower().index("killing ") + 8:]
        author = message.author
        channel = message.channel
        if author.id != self.bot.user.id and channel.id == 841490511390048277:
            return
        # await self.printto(quotee)
        quotee = quotee.lower()
        try:
            if " " in quotee:
                if quotee[:5] == "e bot":
                    quotee = "e bot"
                else:
                    quotee = quotee[:quotee.index(" ")]
                # await self.printto(quotee)
        except Exception as e:
            # await self.printto(e)
            return

        rightcat = None
        if "you" in quotee:
            m = [msg async for msg in channel.history(limit=2)]
            quotee = m.pop()
            # await self.printto(quotee.content)
            quotee = quotee.author.name
            # await self.printto(quotee)
        if "self" in quotee:
            quotee = author.name
        if "e." in quotee or "bot" in quotee:
            skip = True
            rightcat = "images/right cat/ebotdie.png"
        if "mario" in quotee or "mf" in quotee:
            skip = True
            rightcat = "images/right cat/marlefandie.png"
        if "astro" in quotee:
            skip = True
            rightcat = "images/right cat/astrodie.png"
        if "cb" in quotee:
            skip = True
            rightcat = "images/right cat/cbdie.png"
        if "josh" in quotee:
            skip = True
            rightcat = "images/right cat/yosheedie.png"
        if "anth" in quotee or "ante" in quotee:
            skip = True
            rightcat = "images/right cat/anthdie.png"
        if "ed" in quotee:
            rightcat = "images/right cat/edwoskdie.png"
        if "om" in quotee or "gamerside" in quotee:
            skip = True
            rightcat = "images/right cat/omardie.png"
        if "rov" in quotee:
            skip = True
            rightcat = "images/right cat/rovuhdie.png"
        if "m" in quotee and "r" in quotee and not skip:
            rightcat = "images/right cat/meowzadie.png"

        # await self.printto(f"rightcat: {rightcat}")
        if rightcat is None:
            return

        leftcat = None
        match author.id:
            case 405197452833062912: #mariofan
                print("properly assigned mariofan?")
                leftcat = "images/left cat/marlefankil.png"
            case 702906770003198003: #me (uness someone else is reading this, which I DOUBT)
                leftcat = "images/left cat/omarkil.png"
            case 617347174120030208: #rovuh
                leftcat = "images/left cat/rovuhkil.png"
            case 916883861634441286: #edwosk
                leftcat = "images/left cat/edwoskkil.png"
            case 456858402832908301: #CB
                leftcat = "images/left cat/cbkil.png"
            case 721389007426158633: #Josh
                leftcat = "images/left cat/yosheekil.png"
            case 450811106504605706: #Anth
                leftcat = "images/left cat/anthkil.png"
            case 925472450962141195: #mafewerawr
                leftcat = "images/left cat/meowzakil.png"
            case 770464351336923157: #Astro
                leftcat = "images/left cat/astrokil.png"
            case 1377752879963574384: #e bot?
                leftcat = "images/left cat/ebotkil.png"

        if leftcat is None:
            # await message.reply("who r u", ephemeral=True)
            return
        # await self.printto(f"leftcat: {leftcat}")

        if leftcat == "images/left cat/edwoskkil.png" and rightcat == "images/right cat/omardie.png":
            # await self.printto("hard coded image")
            await channel.send(file=discord.File("images/icastgun.png"))
            return
        try:
            leftcat = Image.open(leftcat)
            rightcat = Image.open(rightcat)
            totalwidth = rightcat.width * 2
            new_img = Image.new('RGB', (totalwidth, rightcat.height), color='white')
            new_img.paste(leftcat, (0, 0), leftcat)
            new_img.paste(rightcat, (rightcat.width, 0), rightcat)
            new_img.save(content + ".png")
            if message:
                await channel.send(file=discord.File(content + ".png"))
            os.remove(content+ ".png")
        except Exception as e:
            os.remove(content+ ".png")
            await self.printto(str(e))






async def setup(bot):
    await bot.add_cog(PrintStuff(bot))