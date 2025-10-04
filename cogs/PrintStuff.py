import discord
import mcstatus
from discord.ext import commands, tasks
from typing import Optional
import random
import asyncio
import string
import json
import re
global stopp
import datetime
stopp = False
bluff = False

class PrintStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Print Stuff online")

    #-----------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself to prevent infinite loops
        if message.author == self.bot.user:
            return

        if "today" in message.content.lower() and random.random() < 0.5:
            await self.kasane(message)
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

                print(words)

                for g in words:
                    print(g)
                    if "<@" in g and len(g) > 10:
                        wid = int(g[2:len(g) - 1])
                        print(wid)

                        peep = await self.bot.fetch_user(wid)
                        print(peep)
                        currlist.append(peep)
                    elif "X/6" in g:
                        print("use da failures list")
                        currlist = exlist
                    elif "6/6" in g:
                        print("use almost failures list")
                        currlist = sixlist
                    else:
                        print("frick is that, that ain't an ID")
                print("6/6: ", sixlist)
                print("X/6: ", exlist)
                for guy in exlist:
                    await guy.send("bro failed the wordle smh my head emoji skill issue")
                for guy in sixlist:
                    await guy.send("got the wordle on the last try, not even close")

        # -------------------------------------responds to bluff------------------------------------------#
        global bluff
        if bluff and "e, " in message.content:
            await message.reply("o7 on it", mention_author=False)
            bluff = False

    # ------------------------------------------Bluff----------------------------------------------------------#
    @commands.hybrid_command(name="bluff", brief = "Sometimes ya wanna tell e bot to do something, even if it can't.")
    async def fakeit(self, ctx):
        print("bluff")
        global bluff
        bluff = True
        print("worked")
        await ctx.bot.process_commands(ctx)
    # ----------------------------------Date since made--------------------------------------------#
    @commands.hybrid_group(brief="created")
    async def time(self, ctx):
        print("obsolete")
        await self.bot.process_commands(ctx)
    @time.command()
    async def created(self, ctx):
        await ctx.send(f"<t:{1748565600}:R>")
        await self.bot.process_commands(ctx)

    #-------------------------------Reports mc server status & players when requested--------------------------------#
    @commands.hybrid_group(name = "server")
    async def server(self, ctx):
        print("obsolete")
    @server.command(name = "up")
    async def up(self, ctx):
        sessage = await ctx.send("uh")
        try:
            server = mcstatus.JavaServer.lookup("true-cigarette.gl.joinmc.link")
            server.status().players.online
            if random.random() < 1/90:
                await sessage.edit(content="Nope...")
                return
            else:
                await sessage.edit(content = f"yea {server.status().players.online} {"guys" if server.status().players.online > 1 else "guy" if server.status().players.online == 1 else "nobody"} on there")
            dudes = server.status().players.sample
            dudelist = ""
            if len(dudes) > 1:
                for dude in dudes:
                    dudelist = dudelist + dude.name + ", "
            elif len(dudes) == 1:
                dudelist = dudes[0].name
            if len(dudes) >=1:
                await ctx.send(f"{dudelist}")
            print(server.status())
        except Exception as e:
            if random.random() < 1/90:
                await sessage.edit(content="Yeah One guy one there")
                await sessage.channel.send("Mariofan527")

            else:
                await sessage.edit(content = "nope")

    @up.error
    async def mcstatus_error(self, ctx, error):
        print(f"trying, but {error}")
        await ctx.send("idk something broke")

    #helper command for checking if server is up in main, exists to avoid importing mcstatus *again* in main
    async def sup(self):
        try:
            server = mcstatus.JavaServer.lookup("true-cigarette.gl.joinmc.link")
            server.status().players.online
            print("Server online")
            return 1
        except Exception as e:
            print("Server offline")
            return 0

    #----------------------------------------Hit singer Kasane Teto----------------------------------------------------#

    @commands.hybrid_group(name = "daily")
    async def daily(self, ctx):
        print("obsolete")
    @daily.command(name="teto", brief = "posts the day's teto")
    async def kasane(self, ctx):
        tetos = ["https://tenor.com/view/kasane-gif-10240710281900746822",
                 "https://tenor.com/view/teto-kasane-teto-teto-tuesday-utauloid-gif-25302042",
                 "https://tenor.com/view/kasane-gif-17215851662996724170",
                 "https://tenor.com/view/kasane-gif-5116923922296405686",
                 "https://tenor.com/view/kasane-gif-15454379637737486111",
                 "https://tenor.com/view/kasane-gif-5126225881107011559",
                 "https://tenor.com/view/kasane-gif-17280510370772186668",
                 "https://tenor.com/view/miku-hatsune-miku-anime-dance-silly-gif-7439677361449276795"]
        try:
            if random.random() < 1/20:
                print("wait that's not teto")
                await ctx.reply(tetos[7], mention_author=False)
            else:
                print("teto")
                await ctx.reply(tetos[datetime.date.today().weekday()], mention_author=False)
        except Exception as e:
            print(e)
            print(str(e))

    #-----------------------------------Anim progress tracker-----------------------------------------#
    @tasks.loop(minutes=120)
    async def task(self):
        try:
            channel = self.bot.get_channel(1282010600322629652)
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
                        print("made a file since it wasn't there, running as if was offline")

                day -= 1
                match day:
                    case 3:

                        await channel.send("3 days left :D\n**procrastinate.**")
                    case 2:
                        await channel.send("2 days left :)")
                        await channel.send(file=discord.File("timesatickin.png"))

                    case 1:
                        await channel.send("https://tenor.com/view/majoras-mask-majora-zelda-final-day-gif-26658556")
                    case 0:
                        await channel.send("well, this is ackward. Hopefully you never see this message, 'cause it means I done did messed up and missed the deadline")
                    case _:
                        await channel.send(f"I don't know what I am doing. {day} days left, this message shouldn't be possible to see and only exists for error handling.")

                with open("updayt.txt", "w") as f:
                    f.write(f"{day}")
        except Exception as e:
            print(e)
            print(str(e))

    #--------------------------------Check anim days left----------------------------------------------#
    @commands.hybrid_group(name = "animation")
    async def animation(self, ctx):
        print("obsolete")

    @animation.group(name = "due")
    async def due(self, ctx):
        print("obsolete")
    @due.command(name = "in")
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
                print("made a file since it wasn't there, running as if was offline")
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

    @animation.group(name = "time")
    async def tiempo(self, ctx):
        print("obsolete")
    @tiempo.command(name = "reset")
    async def reset(self, ctx):
        if not (ctx.author.id == 702906770003198003 or ctx.author.id == 405197452833062912):
            await ctx.send("Imma don't think you're allowed to do dat")
            await ctx.send("https://tenor.com/view/luigi-coo-coo-crazy-luigis-mansion-dark-moon-gif-1213275346224547321")
            return
        with open("updayt.txt", "w") as f:
            f.write(f"4")
        await ctx.send("o7 he gets time now")


    # ----------------------------------Deltarune tomorrow--------------------------------------------#
    @commands.hybrid_group(name="deltarune", brief="tomorrow")
    async def deltarune(self, ctx):
        print("obsolete")
        await self.bot.process_commands(ctx)
    @deltarune.command(name="tomorrow", brief="deltarune tomorrow")
    async def tomorrow(self, ctx):
        await ctx.reply("Deltarune tomorrow", mention_author=False)
        await self.bot.process_commands(ctx)

    #----------------------command I made once as a joke to dm mariofan and fake being a bluff but kept---------------#
    sad = [
    "https://tenor.com/view/dog-crying-meme-doggo-crys-megan-soo-crying-dog-gif-5276199764143986284",
    "https://tenor.com/view/sad-walk-gif-24718162",
    "https://tenor.com/view/sadhamstergirl-gif-4231717927828306245",
    "https://tenor.com/view/sad-crying-crying-face-sad-face-sorry-gif-16443666066815353211",
    "https://tenor.com/view/breaking-bad-walter-white-bryan-cranston-sad-oh-no-gif-17379933",
    "https://tenor.com/view/meme-crying-gif-24782561",
    "https://tenor.com/view/%D0%BF%D0%BE%D0%BF%D0%BB%D0%B0%D1%87-gif-14046562056654997205"]
    print(len(sad))

    @commands.group(name = "dm", hidden = True)
    async def sendto(self, ctx):
        print("obsolete")

    @sendto.group(name="mariofan", hidden = True)
    async def mariofan(self, ctx):
        print("obsolete")

    @mariofan.group(name="something")
    async def something(self, ctx):
        print("obsolete")

    @something.group(name="sad")
    async def depressing(self, ctx):
        print("obsolete")

    @depressing.group(name="in")
    async def within(self, ctx):
        print("obsolete")

    @within.group(name="two")
    async def one(self, ctx):
        print("obsolete")

    @one.command(name="minutes")
    async def minute(self, ctx):
        try:
            await ctx.send("o7 on it")
            await asyncio.sleep(120)

            guy = await self.bot.fetch_user(405197452833062912)

            await guy.send(self.sad[random.randint(0, len(self.sad) - 1)])
        except Exception as e:
            print(e)
            print(str(e))

    # ----------------------------------Quote series--------------------------------------------#
    @commands.hybrid_group()
    async def quote(self, ctx):
        print("obsolete")
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
    async def fromQ(self, ctx, guy: discord.Member = discord.ext.commands.parameter(displayed_name="guy",
    description="Dude quoted (if invalid will pull from unknown)"), ephem=False):
        try:
            pulled = 8
            match guy.id:
                case 450811106504605706:
                    pulled = 0
                case 770464351336923157:
                    pulled = 1
                case 456858402832908301:
                    pulled = 2
                case 916883861634441286:
                    pulled = 3
                case 721389007426158633:
                    pulled = 4
                case 405197452833062912:
                    pulled = 5
                case 925472450962141195:
                    pulled = 6
                case 702906770003198003:
                    pulled = 7
                case 8:
                    print("idk")
                    pulled = 8
                case 352236068344561666:
                    pulled = 9
                case 617347174120030208:
                    pulled = 10

            quotelist = self.loadjson(pulled)
            await ctx.send(quotelist[random.randint(0, len(quotelist) - 1)], ephemeral=ephem)
        except Exception as error:
            print("An error occurred:", type(error).__name__)
            print(str(error))



async def setup(bot):
    await bot.add_cog(PrintStuff(bot))