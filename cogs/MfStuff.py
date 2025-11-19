import discord
from discord.ext import commands
import datetime
from typing import Optional
import random
import asyncio
import string
import json

class MfStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_group(guild=discord.Object(1086880428650143765))
    async def asterisk(self):
        print("asterisk")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "Frames" in message.content:
            num = ""
            try:
                num = message.content.split("(+")[1][:-1]
                print(num)
                num = int(num)
                self.incCurrFrames(num)
                await message.add_reaction("🇪")
            except Exception:
                print("what the FRICK are the frames")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mf Stuff online")
    async def getTotalFrames(self):
        return 2158

    async def getCurrFrames(self):
        try:
            with open("mframes.txt", 'r') as f:
                return int(f.readline().strip())
        except FileNotFoundError:
            with open("mframes.txt", "x") as f:
                print("HAAAAAAAAAAANK\n HAAAAAAANNNNNNNNNK YOU FORGOT TO MAKE THE FILE \n HAAAAAAAAAAANNNNNNNNNNKKKKKKKK")
                f.write(str(-1))
        except Exception as e:
            print(e)
            print(type(e))
    @asterisk.command(name = "set_frames", guild=discord.Object(1086880428650143765))
    async def setCurrFrames(self, frames: int):
        with open("mframes.txt", 'w') as f:
            f.write(str(frames))
    @asterisk.command(name = "add_frames", guild=discord.Object(1086880428650143765))
    async def incCurrFrames(self, frameIncrement: int):
        frames = self.getCurrFrames()
        self.setCurrFrames(frames + frameIncrement)
    async def getStartDate(self):
        return datetime.date(2025, 10, 21)
    async def getEndDate(self):
        return datetime.date(2026, 9, 2)
    async def getDate(self):
        return datetime.date.today()
    async def getDaysEllipsed(self):
        start = await self.getStartDate()
        curr = await self.getDate()
        diff = curr - start
        return diff
    async def getDaysLeft(self):
        curr = await self.getDaysEllipsed()
        end = await self.getEndDate()
        return end - curr
    async def getFramesLeft(self):
        frames = await self.getCurrFrames()
        framesLeft = await self.getTotalFrames() - frames
        return framesLeft
    async def getProjPace(self):
        framesLeft = await self.getFramesLeft()
        daysLeft = framesLeft / 7
        return daysLeft
    async def getExpectedFrames(self):
        days = await self.getDaysEllipsed()
        expectedLeft = int(days.days) * 7
        return expectedLeft
    async def getFrameDiff(self):
        expectedLeft = await self.getExpectedFrames()
        currFrames = await self.getCurrFrames()
        difference = currFrames - expectedLeft
        return difference

    async def estimatedate(self): #assuming 7fpd
        daysLater = await self.getProjPace()
        projDate = datetime.date.today() + datetime.timedelta(days=int(daysLater))
        return projDate
    @asterisk.command(guild=discord.Object(1086880428650143765))
    async def progress(self, ctx):#I'm not making the s not appear if in 1 day, future me's syntax error.
        try:
            if ctx.channel.id != 1430330064855236648 and ctx.channel.id != 784923833932709889:
                await ctx.send("wouldn't YOU like to know.")
                return
            print("trying allvals")
        except Exception as e:
            print(e)
        try:
            diff = await self.getFrameDiff()
            print(f"You'll probably finish in {int((await self.getProjPace()))} days, so around {await self.estimatedate()}.\n"
                  + f"You're {(await self.getDaysEllipsed()).days} days in, and {abs(diff)} frame{"s" if (abs(diff) > 1 or abs(diff) == 0) else ""} {"ahead" if diff > 0 else "behind" if diff < 0  else "ahead or behind, no pressure" }"
                           + f"\n (at {await self.getCurrFrames()} frames, avg 7fpd being {await self.getExpectedFrames()})")

            await ctx.send(f"You'll probably finish in {int((await self.getProjPace()))} days, so around {await self.estimatedate()}.\n"
                  + f"You're {(await self.getDaysEllipsed()).days} days in, and {abs(diff)} frame{"s" if (abs(diff) > 1 or abs(diff) == 0) else ""} {"ahead" if diff > 0 else "behind" if diff < 0  else "ahead or behind, no pressure" }"
                           + f"\n (at {await self.getCurrFrames()} frames, avg 7fpd being {await self.getExpectedFrames()})")
        except Exception as e:
            print(e)
            print(type(e))

async def setup(bot):
    await bot.add_cog(MfStuff(bot))