import discord
from discord.ext import commands
from typing import Optional
import random
import asyncio
import string
import json

class SetStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Set Stuff online")

    @commands.hybrid_group(name = "set")
    async def hybrid_group(self, ctx):
        print("obsolete")


    @hybrid_group.group(name = "reaction") #branch for reaction toggles
    async def reaction_group(self, ctx):
        print("obsolete")


#Helper method every setting uses to access nested json of user and set value
    async def setValue(self, ctx, setting, value: bool):
        # the data structure for all settings is a 2d dict.
        # outer array mapping inner array to user ID
        # inner array mapping setting name to value
        outer = {}
        try:
            with open("settings.json", 'r') as f:
                outer = json.load(f)
                inner = outer.get(str(ctx.author.id), {})
                inner[setting] = value
                outer[str(ctx.author.id)] = inner
            with open("settings.json", 'w') as f:
                json.dump(outer, f, indent=2)
                print(f"updated {ctx.author} {setting} to {value}")
                await ctx.send(f"updated {setting} to {value} for {ctx.author}")
        except FileNotFoundError:
            with open("settings.json", "x") as f:
                outer = {str(ctx.author.id): {setting:value}}
                json.dump(outer, f, indent=2)
                print("made a settings file since it wasn't there")
                await ctx.send(f"updated {setting} to {value} for {ctx.author}")
        except Exception as e:
            print(e)
            print(type(e))
            await ctx.send("something broke, ", str(e))



    @reaction_group.command(name = "kys")
    async def kys(self, ctx, value: bool):
        await self.setValue(ctx, "kys", value)

    @reaction_group.command(name = "skillissue")
    async def skillissue(self, ctx, value: bool):
        await self.setValue(ctx, "skillissue", value)

    @reaction_group.command(name = "sadeyes")
    async def sadeyes(self, ctx, value: bool):
        await self.setValue(ctx, "sadeyes", value)

    @reaction_group.command(name = "replyeyes")
    async def replyeyes(self, ctx, value: bool):
        await self.setValue(ctx, "replyeyes", value)

    @reaction_group.command(name = "omaranim")
    async def omaranim(self, ctx, value: bool):
        await self.setValue(ctx, "omaranim", value)




    @hybrid_group.group(name = "chance")
    async def chance_group(self, ctx):
        print("obsolete")


    @chance_group.command(name = "mock")
    async def mock(self, ctx, value: bool):
        await self.setValue(ctx, "mock", value)

    @chance_group.command(name = "tetnot")
    async def tetnot(self, ctx, value: bool):
        await self.setValue(ctx, "tetnot", value)

    @chance_group.command(name = "serverlie")
    async def serverlie(self, ctx, value: bool):
        await self.setValue(ctx, "serverlie", value)

    @chance_group.command(name = "boss")
    async def boss(self, ctx, value: bool):
        await self.setValue(ctx, "boss", value)

    @chance_group.command(name = "boost")
    async def boost(self, ctx, value: bool):
        await self.setValue(ctx, "boost", value)

    @chance_group.command(name="sosad")
    async def sosad(self, ctx, value: bool):
        await self.setValue(ctx, "sosad", value)




    @hybrid_group.group(name = "keyword")
    async def keyword(self, ctx):
        print("obsolete")


    @keyword.command(name = "yoshiandme")
    async def yoshiandme(self, ctx, value: bool):
        await self.setValue(ctx, "yoshiandme", value)

    @keyword.command(name = "debate")
    async def debate(self, ctx, value: bool):
        await self.setValue(ctx, "debate", value)

    @keyword.command(name = "worldismine")
    async def worldismine(self, ctx, value: bool):
        await self.setValue(ctx, "worldismine", value)

    @keyword.command(name = "leavevc")
    async def leavevc(self, ctx, value: bool):
        await self.setValue(ctx, "leavevc", value)

    @keyword.command(name = "fakejoin")
    async def fakejoin(self, ctx, value: bool):
        await self.setValue(ctx, "fakejoin", value)

    @keyword.command(name = "crab")
    async def crab(self, ctx, value: bool):
        await self.setValue(ctx, "crab", value)

    @keyword.command(name = "deltarune")
    async def deltarune(self, ctx, value: bool):
        await self.setValue(ctx, "deltarune", value)

    @keyword.command(name = "tetoday")
    async def tetoday(self, ctx, value: bool):
        await self.setValue(ctx, "tetoday", value)

    async def get_value(self, ctx, member: discord.Member, setting):
        outer = {}
        try:
            with open("settings.json", 'r') as f:
                outer = json.load(f)
                inner = outer.get(str(member.id), {})
                return inner.get(setting, True)
        except FileNotFoundError:
            with open("settings.json", "x") as f:
                outer = {str(member.id): {setting: True}}
                json.dump(outer, f, indent=2)
                print("made a settings file since it wasn't there")
                return True
        except Exception as e:
            print(e)
            print(type(e))
            await ctx.send("something broke, ", str(e))


async def setup(bot):
    await bot.add_cog(SetStuff(bot))