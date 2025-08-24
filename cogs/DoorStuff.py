import discord
from discord.ext import commands
from typing import Optional
import random
from discord.ui import Button, View
import asyncio
import string

class DoorStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot





    async def genViewList(self, ctx, public, ephem):

        async def fail(interaction: discord.Interaction):
            if not public and str(interaction.user.name) != str(ctx.author.name):
                print(f"oi {interaction.user.name} piss off")
                return

            global HSDict
            global scoreDict
            failedStr = "```ansi\n[2;31m[1;31m[1;40m[1;47m[4;31m[4;40m[4;44m[4;40m[4;40mFailed[0m[4;31m[4;40m[0m[4;31m[4;44m[0m[4;31m[4;40m[0m[4;31m[4;47m[0m[1;31m[1;47m[4;31m[0m[1;31m[1;47m[0m[1;31m[1;40m[0m[1;31m[0m[2;31m[0m\n```"

            if scoreDict.get(str(interaction.user.id), 0) == 0:
                try:
                    await retry(interaction, True)
                except Exception as error:
                    print(type(error).__name__)
                    print(str(error))
                return
            print(f"{interaction.user.name} ended with {scoreDict.get(str(interaction.user.id), 0)}")

            with open('HighScore.txt', 'r') as f:
                try:
                    HSDict = eval(f.read())
                except Exception as error:
                    print("An error occurred:", type(error).__name__)
                    print(str(error))

            try:
                if HSDict.get(str(interaction.user.id), 0) < scoreDict.get(str(interaction.user.id), 0):
                    HSDict[str(interaction.user.id)] = scoreDict[str(interaction.user.id)]

                    with open('HighScore.txt', 'w') as f:
                        f.write(str(HSDict))

                if scoreDict.get(str(interaction.user.id), 0) > HSDict.get("High Score", 0):
                    HSDict["High Score"] = scoreDict.get(str(interaction.user.id))
                    HSDict["Holder"] = str(interaction.user.id)
                    with open('HighScore.txt', 'w') as f:
                        f.write(str(HSDict))
                if scoreDict.get(str(interaction.user.id), 0) == HSDict.get("High Score", 0):
                    if str(interaction.user.id) not in HSDict["Holder"]:
                        HSDict["Holder"] = f"{HSDict["Holder"]}  & {interaction.user.id}"
                        with open('HighScore.txt', 'w') as f:
                            f.write(str(HSDict))
                global holder

                try:
                    holder = ctx.guild.get_member(int(HSDict["Holder"]))
                except Exception as error:
                    print(f"An error occurred:", type(error).__name__)
                    holder = "Some guy who ain't here"
                print(str(holder))
                if "None" in str(holder):
                    holder = "Some guy who ain't here"
                if ephem:
                    await interaction.response.edit_message(
                        content=f"{failedStr}High Score: {HSDict["High Score"]} ({holder})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {scoreDict.get(str(interaction.user.id), 0)}.\n Try again?",
                        view=vfail)
                else:
                    await interaction.response.edit_message(
                        content=f"{failedStr}High Score: {HSDict["High Score"]} ({holder})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {scoreDict.get(str(interaction.user.id), 0)}.\n Try again?",
                        view=vfail)


            except Exception as error:
                print("An error occurred:", type(error).__name__)
                print(str(error))

        async def retry(interaction: discord.Interaction, quick = False):
            global scoreDict
            if not public and str(interaction.user.name) != str(ctx.author.name):
                print(f"oi {interaction.user.name} piss off")
                return
            scoreDict[str(interaction.user.id)] = 0
            extra = ""
            if quick:
                print(f"{interaction.user.name} quick restarted")
                extra = " (Quick Restarted)"
            if random.random() < 1 / 2:
                await interaction.response.edit_message(content=f"Score: 0{extra}", view=ri)
            else:
                await interaction.response.edit_message(content=f"Score: 0{extra}", view=le)

        async def quit(interaction: discord.Interaction):
            if str(interaction.user.name) != str(ctx.author.name):
                print(f"oi {interaction.user.name} piss off")
                return
            global scoreDict
            global HSDict

            try:

                await interaction.response.edit_message(
                    content=f"High Score: {HSDict["High Score"]} ({ctx.guild.get_member(int(HSDict["Holder"]))})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {scoreDict.get(str(interaction.user.id), 0)}",
                    view=None)
            except Exception as error:
                print("An error occurred:", type(error).__name__)
                print(str(error))

        async def kill(interaction: discord.Interaction):
            if str(interaction.user.name) != str(ctx.author.name):
                print(f"oi {interaction.user.name} piss off")
                return
            await interaction.message.delete()

        async def reveal(interaction: discord.Interaction):
            global scoreDict
            global HSDict
            try:
                await interaction.response.edit_message(content="Revealed.\n(You can dismiss this now)", view=None)
                await interaction.channel.send(
                    content=f"``{interaction.user} used doors of doom``\nHigh Score: {HSDict["High Score"]} ({ctx.guild.get_member(int(HSDict["Holder"]))})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {scoreDict.get(str(interaction.user.id), 0)}",
                    view=None)

            except Exception as error:
                print("An error occurred:", type(error).__name__)
                print(str(error))

        async def corr(interaction: discord.Interaction):

            print("it at least RAN the function")
            try:
                if not public and str(interaction.user.name) != str(ctx.author.name):
                    print(f"oi {interaction.user.name} piss off")
                    return
                global scoreDict

                scoreDict[str(interaction.user.id)] = scoreDict.get(str(interaction.user.id), 0) + 1
                if random.random() < 1 / 2:
                    await interaction.response.edit_message(content=f"Score:{scoreDict.get(str(interaction.user.id), 0)}",
                                                            view=ri)
                else:
                    await interaction.response.edit_message(content=f"Score:{scoreDict.get(str(interaction.user.id), 0)}",
                                                            view=le)
            except Exception as error:
                print("An error occurred:", type(error).__name__)
                print(str(error))
                print(error)

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

        vfail.add_item(y)

        vfail.add_item(n)

        if ephem:
            vfail.add_item(r)
        else:
            vfail.add_item(k)
        b = Button(label="O🚪")
        b.callback = corr
        b2 = Button(label="X🚪")
        b2.callback = fail


        le.add_item(b)
        le.add_item(b2)

        ri.add_item(b2)
        ri.add_item(b)

        return [ri, le]


    @commands.Cog.listener()
    async def on_ready(self):
        print("Door Stuff online")

    @commands.hybrid_group(name="doors", brief="of doom")
    async def doors_group(self, ctx):
        print("obsolete")

    @doors_group.group(name="of", brief="doom")
    async def of_group(self, ctx):
        print("obsolete")

    @of_group.command(name="scores")
    async def scores(self, ctx):
        global HSDict
        with open('HighScore.txt', 'r') as f:
            try:
                HSDict = eval(f.read())
            except Exception as error:
                print("An error occurred:", type(error).__name__)
                print(str(error))
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
                    print(str(error))

            scores = str(display)
            scores = scores.replace("'", "").replace(",", "\n")
            scores = scores.replace("{", "").replace("}", "")

            await ctx.send(scores)
        except Exception as error:
            print("An error occurred:", type(error).__name__)

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
        print(f"{ctx.author.name} is {ephem} a ghost")
        views = []
        try:
            views = await self.genViewList(ctx, public, ephem)
        except Exception as error:
            print("An error occurred:", type(error).__name__)
            print(str(error))


        try:
           if random.random() < 1 / 2:
                await ctx.send("Doors of doom\n https://imgur.com/a/nfXbOqZ", view=views[1], ephemeral=ephem)
           else:
                await ctx.send("Doors of doom\n https://imgur.com/a/nfXbOqZ", view=views[0], ephemeral=ephem)
        except Exception as error:
            print("An error occurred:", type(error).__name__)
            print(str(error))

    #TODO: adapt genViewList to have a daily mode & default mode, so this frickin thing can finally work
    @of_group.command(name="daily")
    async def daily(self, ctx, ephem: Optional[bool]):
        global scoreDict2
        if "true" in str(ephem).lower():
            ephem = True
        else:
            ephem = False

        scoreDict2 = {str(ctx.author.name): 0}

        done = {}
        with open('pVars.json', 'r') as f:
            try:
                done = eval(f.read())
                done = done["Did Daily"]
            except Exception as error:
                print("An error occurred:", type(error).__name__)
                print(str(error))
            print("made it past done read")
            print(done)

            if done.get(ctx.author.id, False):
                await ctx.send("Daily has already been done")
                return
            else:
                done[ctx.author.id] = False
            print("made it past done check")

            async def failtwo(interaction):
                if str(interaction.user.name) != str(ctx.author.name):
                    print(f"oi {interaction.user.name} piss off")
                    return

                failedStr = "```ansi\n[2;31m[1;31m[1;40m[1;47m[4;31m[4;40m[4;44m[4;40m[4;40mFailed[0m[4;31m[4;40m[0m[4;31m[4;44m[0m[4;31m[4;40m[0m[4;31m[4;47m[0m[1;31m[1;47m[4;31m[0m[1;31m[1;47m[0m[1;31m[1;40m[0m[1;31m[0m[2;31m[0m\n```"

                if scoreDict2.get(str(interaction.user.id), 0) == 0:
                    await interaction.response.edit_message("YOU FAI- oh quick restarts still exist, luckily. Score: 0")
                    return
                print(f"{interaction.user.name} ended with {scoreDict2.get(str(interaction.user.id), 0)}")
                global HSDict
                with open('HighScore.txt', 'r') as f:
                    try:
                        HSDict = eval(f.read())
                    except Exception as error:
                        print("An error occurred:", type(error).__name__)
                        print(str(error))

                try:
                    if HSDict.get(str(interaction.user.id), 0) < scoreDict2.get(str(interaction.user.id), 0):
                        HSDict[str(interaction.user.id)] = scoreDict2[str(interaction.user.id)]

                        with open('HighScore.txt', 'w') as f:
                            f.write(str(HSDict))
                    if scoreDict2.get(str(interaction.user.id), 0) > HSDict.get("High Score", 0):
                        HSDict["High Score"] = scoreDict2.get(str(interaction.user.id))
                        HSDict["Holder"] = str(interaction.user.id)
                        with open('HighScore.txt', 'w') as f:
                            f.write(str(HSDict))
                    if scoreDict2.get(str(interaction.user.id), 0) == HSDict.get("High Score", 0):
                        if str(interaction.user.id) not in HSDict["Holder"]:
                            HSDict["Holder"] = f"{HSDict["Holder"]}  & {interaction.user.name}"
                            with open('HighScore.txt', 'w') as f:
                                f.write(str(HSDict))
                    print("made it past hs")

                    with open('didDaily.json', 'w') as f:
                        try:
                            done[ctx.author.id] = True
                            f.write(str(done))
                        except Exception as error:
                            print("An error occurred:", type(error).__name__)
                            print(str(error))
                    print("made it past done check")

                    await interaction.response.edit_message(
                        content=f"{failedStr}High Score: {HSDict["High Score"]} ({HSDict["Holder"]})\nPersonal Best: {HSDict.get(str(interaction.user.id), 0)}\nScore: {scoreDict2.get(str(interaction.user.id), 0)}",
                        view=None)

                except Exception as error:
                    print("An error occurred:", type(error).__name__)
                    print(str(error))

            print("made it past fail")

            async def corrtwo(interaction):
                if str(interaction.user.name) != str(ctx.author.name):
                    print(f"oi {interaction.user.name} piss off")
                    return
                print("past piss")
                global scoreDict2
                print("past global")
                try:
                    scoreDict2[str(interaction.user.id)] = scoreDict2.get(str(interaction.user.id), 0) + 1
                except Exception as error:
                    print("An error occurred:", type(error).__name__)
                    print(str(error))

                print("past increment")
                if random.random() < 1 / 2:
                    print("pre edit")
                    await interaction.response.edit_message(
                        content=f"Score:{scoreDict2.get(str(interaction.user.id), 0)}", view=ri)
                else:
                    print("pre edit")
                    await interaction.response.edit_message(
                        content=f"Score:{scoreDict2.get(str(interaction.user.id), 0)}", view=le)

            print("made it past corr")
            ri = View(timeout=60)
            le = View(timeout=60)

            print("made it to buttons")

            b = Button(label="🚪")
            b.callback = corrtwo
            b2 = Button(label="🚪")
            b2.callback = failtwo
            le.add_item(b)
            le.add_item(b2)
            ri.add_item(b2)
            ri.add_item(b)
            print("made it to rando")
            if random.random() < 1 / 2:
                await ctx.send("Doors of DAILY\n*One* shot per run daily, feeling lucky?\n https://imgur.com/a/nfXbOqZ",
                               view=ri, ephemeral=ephem)
            else:
                await ctx.send("Doors of DAILY\n*One* shot per run daily, feeling lucky?\n https://imgur.com/a/nfXbOqZ",
                               view=le, ephemeral=ephem)

        print(f"{ctx.author.name} is {ephem} a ghost")

async def setup(bot):
    await bot.add_cog(DoorStuff(bot))