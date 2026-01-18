import discord
from discord.ext import commands, tasks
from typing import Optional
import random
from discord.ui import Button, View
import asyncio
import string
import datetime

class DoorStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timepass.start()

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
                    try:
                        if gdict.get(str(interaction.user.id), 0) >=2:
                            extra = extra + "\n you may now use https://discord.com/channels/773015467753209888/1461631744955514932"
                            channelrole = ctx.author.guild.get_role(1462230075503149299)
                            await interaction.user.add_roles(channelrole)
                            doorlist = {}
                            try:
                                try:
                                    with open("opendoors.json", 'r') as f:
                                        doorlist = eval(f.read())
                                    doorlist[str(ctx.author.id)] = 27
                                    with open("opendoors.json", 'w') as f:
                                        f.write(str(doorlist))
                                except FileNotFoundError:
                                    with open("opendoors.json", "x") as f:
                                        doorlist[str(ctx.author.id)] = 27
                                        f.write(str(doorlist))
                                        await self.printto("made a file since it wasn't there")
                                except ValueError:
                                    await self.printto(f"something went HORRIBLY wrong with open doors somehow")
                            except Exception as e:
                                await self.printto(f"{e}\n{str(e)}")
                                return
                        elif gdict.get(str(interaction.user.id), 0) <= -4:
                            channelrole = ctx.author.guild.get_role(1462230075503149299)
                            await ctx.author.remove_roles(channelrole)
                            extra = extra + f"\n btw you get to steal {round(gdict.get(str(interaction.user.id), 0) * (-2.718281828))} hours from someone with doors time commands :D"
                            doorlist = {}
                            try:
                                try:
                                    with open("opendoors.json", 'r') as f:
                                        doorlist = eval(f.read())
                                    doorlist[str(ctx.author.id)] = round(gdict.get(str(interaction.user.id), 0) * 2.718281828)
                                    with open("opendoors.json", 'w') as f:
                                        f.write(str(doorlist))
                                except FileNotFoundError:
                                    with open("opendoors.json", "x") as f:
                                        doorlist[str(ctx.author.id)] = round(gdict.get(str(interaction.user.id), 0) * 2.718281828)
                                        f.write(str(doorlist))
                                        await self.printto("made a file since it wasn't there")
                                except ValueError:
                                    await self.printto(f"something went HORRIBLY wrong with open doors somehow")
                            except Exception as e:
                                await self.printto(f"{e}\n{str(e)}")
                                return
                    except Exception as e:
                        await self.printto(str(e))



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
                other = ""
                if not public and str(interaction.user.name) != str(ctx.author.name):
                    await self.printto(f"oi {interaction.user.name} piss off")
                    return
                if gdict[str(interaction.user.id)] < 0 and dailymode:
                    gdict[str(interaction.user.id)] -= 1
                else:
                    gdict[str(interaction.user.id)] = gdict.get(str(interaction.user.id), 0) + 1
                    if gdict.get(str(interaction.user.id), 0) >=5:
                        times = {}
                        try:
                            with open("opendoors.json", 'r') as f:
                                times = eval(f.read())
                            channelrole = ctx.author.guild.get_role(1462230075503149299)
                            if times[str(interaction.user.id)] >=0:
                                await ctx.author.add_roles(channelrole)
                                times[str(interaction.user.id)] = times.get(str(interaction.user.id), 0) + 1
                                other = "\n(also +1 https://discord.com/channels/773015467753209888/1461631744955514932 hours for every point past here)"
                            else:
                                other = "\n(also +1 https://discord.com/channels/773015467753209888/1461631744955514932 hours you can steal for every point past here)"
                                times[str(interaction.user.id)] = times.get(str(interaction.user.id), 0) - 1



                        except FileNotFoundError:
                            await self.printto("file didn't exist, making and setting to 1")
                            times[str(interaction.user.id)] = 1
                            channelrole = ctx.author.guild.get_role(1462230075503149299)
                            await ctx.author.add_roles(channelrole)

                        await self.printto(f"their hours are now at {times.get(str(interaction.user.id), 0)}")
                        with open("opendoors.json", 'w') as f:
                            f.write(str(times))

                if random.random() < 1 / 2:
                    await interaction.response.edit_message(content=f"Score:{gdict.get(str(interaction.user.id), 0)}{other}",
                                                            view=ri)
                else:
                    await interaction.response.edit_message(content=f"Score:{gdict.get(str(interaction.user.id), 0)}{other}",
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
        await ctx.typing()

        pacific = discord.utils.get(ctx.guild.roles, name="Pacific Time -8")
        central = discord.utils.get(ctx.guild.roles, name="Central Time -6")
        eastern = discord.utils.get(ctx.guild.roles, name="Eastern Time -5")
        mountain = discord.utils.get(ctx.guild.roles, name="Mountain Time -7")
        ceneuro = discord.utils.get(ctx.guild.roles, name="Central European Time +1")
        t = datetime.datetime.now().hour
        d = datetime.datetime.now().day

        if pacific in ctx.author.roles:
            #do nothing
            await asyncio.sleep(0.001)
        elif central in ctx.author.roles:
            if t >= 22:
                d +=1
        elif eastern in ctx.author.roles:
            if t >= 21:
                d += 1
        elif mountain in ctx.author.roles:
            if t == 0:
                d -= 1
        elif ceneuro in ctx.author.roles:
            if t <= 3:
                d-=1


        donelist = {}
        try:
            try:
                with open("donely.json", 'r') as f:
                    donelist = eval(f.read())
            except FileNotFoundError:
                with open("donely.json", "x") as f:
                    donelist[str(ctx.author.id)] = -1
                    f.write(str(donelist))
                    await self.printto("made a file since it wasn't there")
            except ValueError:
                await self.printto(f"something went HORRIBLY wrong with donely somehow")
        except Exception as e:
            await self.printto(f"{e}\n{str(e)}")
            return

        try:
            if donelist[str(ctx.author.id)] == d:
                await ctx.send("ya did it already -. -")
                return
            else:
                donelist[str(ctx.author.id)] = d
        except KeyError:
            await self.printto("person not being tracked, adding to file and allowing to play")
            donelist[str(ctx.author.id)] = d
        with open("donely.json", 'w') as f:
            f.write(str(donelist))




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


        try:
           if random.random() < 1 / 2:
                await ctx.send("Doors of Daily, think you're lucky?\nhttps://tenor.com/view/oneshot-ballin-gif-8940602852183524649", view=views[1], ephemeral=ephem)
           else:
                await ctx.send("Doors of Daily, think you're lucky?\nhttps://tenor.com/view/oneshot-ballin-gif-8940602852183524649", view=views[0], ephemeral=ephem)
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)
            await self.printto(str(error))

    @tasks.loop(minutes=60)  # Runs every hour
    async def timepass(self):
        await self.printto("updating door hours...")
        times = {}
        try:
            mcb = await self.bot.fetch_guild(773015467753209888)
            channelrole = mcb.get_role(1462230075503149299)

        except Exception as e:
            print(str(e))
        try:
            with open("opendoors.json", 'r') as f:
                times = eval(f.read())
        except FileNotFoundError:
            await self.printto("file doesn't exist, ignoring...")
            return


        for key in times:
            try:
                sucker = await mcb.fetch_member(key)

                await self.printto(f"{sucker.display_name} before: {times[key]}")
            except Exception as e:
                await self.printto(str(e))

            if times[key] > 0:
                times[key] -= 1
            if times[key] <= 0:
                try:
                    await sucker.remove_roles(channelrole)
                except Exception as e:

                    await self.printto(str(e))
                if times[key] < 0:
                    times[key] = int(times[key]/2)
            await self.printto(f"{sucker.display_name} after: {times[key]}")

        with open("opendoors.json", 'w') as f:
            f.write(str(times))
        await self.printto("doors loop successful")


    @doors_group.group(name="time", brief="steal | list")
    async def time_group(self, ctx):
        await self.printto("obsolete")

    @time_group.command(name="list")
    async def time_list(self, ctx):
        doorlist = {}
        with open('opendoors.json', 'r') as f:
            try:
                doorlist = eval(f.read())
            except Exception as error:
                await self.printto("An error occurred:", type(error).__name__)
                await self.printto(str(error))
        try:
            tmp = doorlist.copy()

            tmp = dict(sorted(tmp.items(), key=lambda item: item[1], reverse=True))
            display = {}
            for s in tmp:
                try:
                    display[ctx.guild.get_member(int(s)).display_name] = tmp[s]
                except Exception as error:
                    await self.printto(str(error))

            scores = str(display)
            scores = scores.replace("'", "").replace(",", " hours\n")
            scores = scores.replace("{", "").replace("}", " hours")

            await ctx.send(scores)
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)

    @time_group.command(name="steal")
    async def steal(self, ctx, sucker: discord.Member):
        doorlist = {}
        with open('opendoors.json', 'r') as f:
            try:
                doorlist = eval(f.read())
            except Exception as error:
                await self.printto("An error occurred:", type(error).__name__)
                await self.printto(str(error))
                await ctx.send(str(error))
                return
        ours = doorlist.get(str(ctx.author.id), 0)
        if ours >= 0:
            await ctx.send("you gotta get -4 or beyond in daily to steal from people\n(that lets you steal your score * e hours)\n y'ain't even broke -. -")
            return

        hours = doorlist.get(str(sucker.id), 0)
        if hours == 0:
            await ctx.send("bro they literally have nothing to steal pick someone else\n(maybe run /doors time list)")
            return
        elif hours < 0:
            await ctx.send("bro they're (also) in DEBT\npick someone else.\nIf *only* there was a doors time list command to see who has hours...")
            return

        result = hours + ours
        channelrole = ctx.author.guild.get_role(1462230075503149299)

        if result > 0:
            await ctx.send(f"you steal {abs(ours)} hours from {sucker.display_name}.")
            doorlist[str(ctx.author.id)] = abs(ours)
            doorlist[str(sucker.id)] = result
        elif result < 0:
            await ctx.send(f"they were kinda broke so you only steal {hours} hour{"s" if hours >  0 else ""} (everything they had).")
            doorlist[str(ctx.author.id)] = hours
            doorlist[str(sucker.id)] = 0
            sucker.remove_roles(channelrole)

        elif result == 0:
            await ctx.send(f"you steal exactly every single hour they had")
            doorlist[str(ctx.author.id)] = abs(ours)
            doorlist[str(sucker.id)] = 0
            sucker.remove_roles(channelrole)

        await ctx.author.add_roles(channelrole)
        with open("opendoors.json", 'w') as f:
            f.write(str(doorlist))


async def setup(bot):
    await bot.add_cog(DoorStuff(bot))