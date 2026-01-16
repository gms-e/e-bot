import discord
from discord.ext import commands
from typing import Optional
import random
from discord.ui import Button, View
import asyncio
import string
import datetime

class DoorStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def printto(self, m: str):
        print(m)
        channel = await self.bot.fetch_channel(1434085107240534121)
        if channel is None:
            channel = await self.bot.get_channel(1434085107240534121)

        try:
            await channel.send(m)
        except Exception as error:
            print(str(error))
            try:
                await channel.send(str(error))
            except Exception as error:
                print("ok that's enough try catch")

    async def genViewList(self, ctx, public, ephem, gdict, dailymode):

        async def fail(interaction: discord.Interaction):
            if not public and str(interaction.user.name) != str(ctx.author.name):
                await self.printto(f"oi {interaction.user.name} piss off")
                return

            global HSDict
            failedStr = "```ansi\n[2;31m[1;31m[1;40m[1;47m[4;31m[4;40m[4;44m[4;40m[4;40mFailed[0m[4;31m[4;40m[0m[4;31m[4;44m[0m[4;31m[4;40m[0m[4;31m[4;47m[0m[1;31m[1;47m[4;31m[0m[1;31m[1;47m[0m[1;31m[1;40m[0m[1;31m[0m[2;31m[0m\n```"

            if gdict.get(str(interaction.user.id), 0) == 0:
                try:
                    await retry(interaction, True)
                except Exception as error:
                    await self.printto(type(error).__name__)
                    await self.printto(str(error))
                return
            await self.printto(f"{interaction.user.name} ended with {gdict.get(str(interaction.user.id), 0)}")

            with open('HighScore.txt', 'r') as f:
                try:
                    HSDict = eval(f.read())
                except Exception as error:
                    await self.printto("An error occurred:", type(error).__name__)
                    await self.printto(str(error))

            try:
                if HSDict.get(str(interaction.user.id), 0) < gdict.get(str(interaction.user.id), 0):
                    HSDict[str(interaction.user.id)] = gdict[str(interaction.user.id)]

                    with open('HighScore.txt', 'w') as f:
                        f.write(str(HSDict))

                if gdict.get(str(interaction.user.id), 0) > HSDict.get("High Score", 0):
                    HSDict["High Score"] = gdict.get(str(interaction.user.id))
                    HSDict["Holder"] = str(interaction.user.id)
                    with open('HighScore.txt', 'w') as f:
                        f.write(str(HSDict))
                if gdict.get(str(interaction.user.id), 0) == HSDict.get("High Score", 0):
                    if str(interaction.user.id) not in HSDict["Holder"]:
                        HSDict["Holder"] = f"{HSDict['Holder']}  & {interaction.user.id}"
                        with open('HighScore.txt', 'w') as f:
                            f.write(str(HSDict))
                global holder

                try:
                    holder = ctx.guild.get_member(int(HSDict["Holder"]))
                except Exception as error:
                    await self.printto(f"An error occurred:", type(error).__name__)
                    holder = "Some guy who ain't here"
                await self.printto(str(holder))
                if "None" in str(holder):
                    holder = "Some guy who ain't here"

                extra = "Try again?"
                if dailymode:
                    extra = "Try aga-\noh wait you CAN'T"
                if ephem:
                    await interaction.response.edit_message(
                        content=f"{failedStr}High Score: {HSDict['High Score']} ({holder})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {gdict.get(str(interaction.user.id), 0)}.\n{extra}",
                        view=vfail)
                else:
                    await interaction.response.edit_message(
                        content=f"{failedStr}High Score: {HSDict['High Score']} ({holder})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {gdict.get(str(interaction.user.id), 0)}.\n{extra}",
                        view=vfail)


            except Exception as error:
                await self.printto("An error occurred:", type(error).__name__)
                await self.printto(str(error))

        async def retry(interaction: discord.Interaction, quick = False):
            if not public and str(interaction.user.name) != str(ctx.author.name):
                await self.printto(f"oi {interaction.user.name} piss off")
                return
            if gdict[str(interaction.user.id)] <= 0 and dailymode:
                gdict[str(interaction.user.id)] -= 1
            else:
                gdict[str(interaction.user.id)] = 0
            extra = ""
            if quick:
                await self.printto(f"{interaction.user.name} quick restarted")
                if dailymode:
                    extra = " (YOU FA- actually, you know what?)\n(NEGATIVE TIME)"
                else:
                    extra = " (Quick Restarted)"
            if random.random() < 1 / 2:
                await interaction.response.edit_message(content=f"Score: {gdict[str(interaction.user.id)]}{extra}", view=ri)
            else:
                await interaction.response.edit_message(content=f"Score: {gdict[str(interaction.user.id)]}{extra}", view=le)

        async def quit(interaction: discord.Interaction):
            if str(interaction.user.name) != str(ctx.author.name):
                await self.printto(f"oi {interaction.user.name} piss off")
                return
            global HSDict

            try:

                await interaction.response.edit_message(
                    content=f"High Score: {HSDict['High Score']} ({ctx.guild.get_member(int(HSDict['Holder']))})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {gdict.get(str(interaction.user.id), 0)}",
                    view=None)
            except Exception as error:
                await self.printto("An error occurred:", type(error).__name__)
                await self.printto(str(error))

        async def kill(interaction: discord.Interaction):
            if str(interaction.user.name) != str(ctx.author.name):
                await self.printto(f"oi {interaction.user.name} piss off")
                return
            await interaction.message.delete()

        async def reveal(interaction: discord.Interaction):
            global HSDict
            try:
                await interaction.response.edit_message(content="Revealed.\n(You can dismiss this now)", view=None)

                await interaction.channel.send(
                    content=f"``{interaction.user} used doors of {"daily" if dailymode else "doom" }``\nHigh Score: {HSDict['High Score']} ({ctx.guild.get_member(int(HSDict['Holder']))})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {gdict.get(str(interaction.user.id), 0)}",
                    view=None)

            except Exception as error:
                await self.printto("An error occurred:", type(error).__name__)
                await self.printto(str(error))

        async def corr(interaction: discord.Interaction):

            try:
                if not public and str(interaction.user.name) != str(ctx.author.name):
                    await self.printto(f"oi {interaction.user.name} piss off")
                    return
                if gdict[str(interaction.user.id)] < 0 and dailymode:
                    gdict[str(interaction.user.id)] -= 1
                else:
                    gdict[str(interaction.user.id)] = gdict.get(str(interaction.user.id), 0) + 1
                if random.random() < 1 / 2:
                    await interaction.response.edit_message(content=f"Score:{gdict.get(str(interaction.user.id), 0)}",
                                                            view=ri)
                else:
                    await interaction.response.edit_message(content=f"Score:{gdict.get(str(interaction.user.id), 0)}",
                                                            view=le)
            except Exception as error:
                await self.printto("An error occurred:", type(error).__name__)
                await self.printto(str(error))
                await self.printto(error)

        vfail = View(timeout=50)
        ri = View(timeout=120)
        le = View(timeout=120)

        y = Button(label="Retry", style=discord.ButtonStyle.green)
        y.callback = retry

        n = Button(label="Save & Quit", style=discord.ButtonStyle.blurple)
        n.callback = quit

        k = Button(label="X", style=discord.ButtonStyle.red)
        k.callback = kill

        r = Button(label="Reveal", style=discord.ButtonStyle.gray)
        r.callback = reveal

        if not dailymode:
            vfail.add_item(y)

        vfail.add_item(n)

        if ephem:
            vfail.add_item(r)
        else:
            vfail.add_item(k)
        b = Button(label="🚪")
        b.callback = corr
        b2 = Button(label="🚪")
        b2.callback = fail


        le.add_item(b)
        le.add_item(b2)

        ri.add_item(b2)
        ri.add_item(b)

        return [ri, le]


    @commands.Cog.listener()
    async def on_ready(self):
        await self.printto("Door Stuff online")

    @commands.hybrid_group(name="doors", brief="of doom | of scores | of daily")
    async def doors_group(self, ctx):
        await self.printto("obsolete")

    @doors_group.group(name="of", brief="doom | scores | daily")
    async def of_group(self, ctx):
        await self.printto("obsolete")

    @of_group.command(name="scores")
    async def scores(self, ctx):
        global HSDict
        with open('HighScore.txt', 'r') as f:
            try:
                HSDict = eval(f.read())
            except Exception as error:
                await self.printto("An error occurred:", type(error).__name__)
                await self.printto(str(error))
        try:
            tmp = HSDict.copy()
            del tmp["Holder"]

            tmp = dict(sorted(tmp.items(), key=lambda item: item[1], reverse=True))
            display = {}
            for s in tmp:
                try:
                    if "High Score" in s:
                        display[s] = tmp[s]
                        continue
                    display[ctx.guild.get_member(int(s)).display_name] = tmp[s]
                except Exception as error:
                    await self.printto(str(error))

            scores = str(display)
            scores = scores.replace("'", "").replace(",", "\n")
            scores = scores.replace("{", "").replace("}", "")

            await ctx.send(scores)
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)

    @of_group.command(name="doom")
    async def doom(self, ctx, ephem: Optional[bool], public: Optional[bool]):
        public
        if "true" in str(ephem).lower():
            ephem = True
        else:
            ephem = False
        if "true" in str(public).lower():
            public = True
        else:
            public = False
        global scoreDict
        global HSDict
        scoreDict = {str(ctx.author.id): 0}
        await self.printto(f"{ctx.author.name} is {ephem} a ghost")
        views = []
        try:
            views = await self.genViewList(ctx, public, ephem, scoreDict, False)
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)
            await self.printto(str(error))


        try:
           if random.random() < 1 / 2:
                await ctx.send("Doors of doom\n https://imgur.com/a/nfXbOqZ", view=views[1], ephemeral=ephem)
           else:
                await ctx.send("Doors of doom\n https://imgur.com/a/nfXbOqZ", view=views[0], ephemeral=ephem)
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)
            await self.printto(str(error))

    @of_group.command(name="daily")
    async def daily(self, ctx, ephem: Optional[bool]):
        #checks if day has changed and resets dailist if so
        tempmes = await ctx.send("_ _", ephemeral=True)
        currday = datetime.datetime.today().weekday()
        serday = -1
        # TODO: combine all persistent memory into one dict JSON file, because this is getting ridiculous

        try:
            with open("weeknum.txt", 'r') as f:
                line = f.readline()
                serday = int(line.strip())  # Strip whitespace and convert to int
        except FileNotFoundError:
            with open("weeknum.txt", "x") as f:
                f.write(f"{datetime.datetime.today().weekday()}")
                serday = 999
                await self.printto("made a file since it wasn't there, running as if different day")
        except ValueError:
            await self.printto(f"something went HORRIBLY wrong with the file somehow")
        if currday == serday:
            await self.printto("same day")
        else:
            with open("weeknum.txt", "w") as f:
                f.write(f"{datetime.datetime.today().weekday()}")
            with open("dailist.json", "w") as f:
                f.write(str({}))


        #checks dailist regardless of day change or not
        done = {}
        try:
            with open("dailist.json", "r") as f:
                done = eval(f.read())
        except FileNotFoundError as error:
            await self.printto(str(error))
            await self.printto ("file doesn't exist so we makin' it and moving on")
            with open("dailist.json", "w") as f:
                f.write(str({}))


        if done.get(str(ctx.author.id), False):
            await ctx.send("Ya did it already -. -", ephemeral=ephem)
            return
        else:
            try:
                with open("dailist.json", "w") as f:
                    await self.printto("assigning done")
                    done[str(ctx.author.id)] = True
                    await self.printto("done")
                    f.write(str(done))
            except Exception as error:
                await self.printto(f"An error occurred:", type(error).__name__)
                await self.printto(str(error))
        await self.printto("made it past done check")

        if "true" in str(ephem).lower():
            ephem = True
        else:
            ephem = False
        global scoreDict2
        scoreDict2 = {str(ctx.author.id): 0}

        await self.printto(f"{ctx.author.name} is {ephem} a ghost")
        views = []
        try:
            views = await self.genViewList(ctx, False, ephem, scoreDict2, True)
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)
            await self.printto(str(error))

        await tempmes.delete()
        try:
           if random.random() < 1 / 2:
                await ctx.send("Doors of Daily, think you're lucky?\nhttps://tenor.com/view/oneshot-ballin-gif-8940602852183524649", view=views[1], ephemeral=ephem)
           else:
                await ctx.send("Doors of Daily, think you're lucky?\nhttps://tenor.com/view/oneshot-ballin-gif-8940602852183524649", view=views[0], ephemeral=ephem)
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)
            await self.printto(str(error))


async def setup(bot):
    await bot.add_cog(DoorStuff(bot))