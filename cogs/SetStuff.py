import discord
from discord import app_commands
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

    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def hybrid_group(self, ctx):
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

    @hybrid_group.command(name = "tings", brief = "view settings (non displayed settings are true)")
    async def tings(self, ctx):
        outer = {}
        try:
            with open("settings.json", 'r') as f:
                outer = json.load(f)
                inner = outer.get(str(ctx.author.id), {})
                response = str(inner)
                response = response.replace("'", "")
                response = response.replace("{", "")
                response = response.replace("}", "")
                response = response.replace(", ", "\n")
                response = response.replace(":", " =")
                await ctx.send(response)
        except FileNotFoundError:
            with open("settings.json", "x") as f:
                outer = {str(ctx.author.id): {}}
                json.dump(outer, f, indent=2)
                print("made a settings file since it wasn't there")
                await ctx.send(str({}))
        except Exception as e:
            print(e)
            print(type(e))
            await ctx.send("something broke, ", str(e))

    @hybrid_group.group(name = "link", brief = "dmtochat | chattodm")
    async def link(self, ctx):
        print("obsolete")

    @link.command(name = "dmtochat", brief = "send dms to anon channel")
    async def dmtochat(self, ctx, value: bool):
        await self.setValue(ctx, "dmtochat", value)

    @link.command(name = "chattodm", brief = "sends messages from anon channel to dms")
    async def chattodm(self,  ctx, value:bool):
        await self.setValue(ctx, "chattodm", value)

        outer = {}
        try:
            with open("settings.json", 'r') as f:
                outer = json.load(f)
                people = outer.get("dms", [])
                if value and ctx.author.id not in people:
                    people.append(ctx.author.id)
                elif not value and ctx.author.id in people:
                    people.remove(ctx.author.id)
                outer["dms"] = people
            with open("settings.json", 'w') as f:
                json.dump(outer, f, indent=2)
        except Exception as e:
            print(e)
            print(type(e))
            await ctx.send("something broke, ", str(e))

    @hybrid_group.group(name = "reaction", brief = "branch for toggling message reactions")
    async def reaction_group(self, ctx):
        print("obsolete")


    @reaction_group.command(name = "kys", brief = "toggles kys reaction")
    async def kys(self, ctx, value: bool):
        await self.setValue(ctx, "kys", value)

    @reaction_group.command(name = "skillissue", brief = "toggles skill issue reaction for all keywords")
    async def skillissue(self, ctx, value: bool):
        await self.setValue(ctx, "skillissue", value)

    @reaction_group.command(name = "sadeyes", brief = "toggles eyes from saying so sad")
    async def sadeyes(self, ctx, value: bool):
        await self.setValue(ctx, "sadeyes", value)

    @reaction_group.command(name = "replyeyes", brief = "toggles eye reaction from pinging e bot")
    async def replyeyes(self, ctx, value: bool):
        await self.setValue(ctx, "replyeyes", value)

    @reaction_group.command(name = "omaranim", brief = "toggles response to omar animating in sentence")
    async def omaranim(self, ctx, value: bool):
        await self.setValue(ctx, "omaranim", value)




    @hybrid_group.group(name = "chance", brief = "branch for all random chance 'features'")
    async def chance_group(self, ctx):
        print("obsolete")


    @chance_group.command(name = "mock", brief = "toggles 1/1000 mock chance")
    async def mock(self, ctx, value: bool):
        await self.setValue(ctx, "mock", value)

    @chance_group.command(name = "tetnot", brief = "toggles 1/20 chance to get miku")
    async def tetnot(self, ctx, value: bool):
        await self.setValue(ctx, "tetnot", value)

    @chance_group.command(name = "serverlie", brief = "toggles 1/90 chance for server up to lie")
    async def serverlie(self, ctx, value: bool):
        await self.setValue(ctx, "serverlie", value)

    @chance_group.command(name = "boss", brief = "toggles 1/100 chance for link boss music")
    async def boss(self, ctx, value: bool):
        await self.setValue(ctx, "boss", value)

    @chance_group.command(name = "boost", brief = "toggles 1/84 chance boost replaces yoshi and me")
    async def boost(self, ctx, value: bool):
        await self.setValue(ctx, "boost", value)

    @chance_group.command(name="sosad", brief = "toggles chance to be asked how sad")
    async def sosad(self, ctx, value: bool):
        await self.setValue(ctx, "sosad", value)

    @chance_group.command(name = "fakejoin", brief = "toggles 1/500 chance I don't think has even happened ONCE since adding it, so why bother")
    async def fakejoin(self, ctx, value: bool):
        await self.setValue(ctx, "fakejoin", value)



    @hybrid_group.group(name = "keyword", brief = "toggles non command keywords")
    async def keyword(self, ctx):
        print("obsolete")


    @keyword.command(name = "yoshiandme", brief = "removes 'play yoshi and me' in message check, gotta use jimjam now")
    async def yoshiandme(self, ctx, value: bool):
        await self.setValue(ctx, "yoshiandme", value)

    @keyword.command(name = "debate", brief = "toggles 'play boost debate' in message check, gotta use / command now")
    async def debate(self, ctx, value: bool):
        await self.setValue(ctx, "debate", value)

    # @keyword.command(name = "worldismine", brief = "toggles keywords for world is mine song, bet you forgot those were around")
    # async def worldismine(self, ctx, value: bool):
    #     await self.setValue(ctx, "worldismine", value)

    @keyword.command(name = "leavevc", brief = "toggles keywords to make bot leave vc, which everyone forgets are around ._.")
    async def leavevc(self, ctx, value: bool):
        await self.setValue(ctx, "leavevc", value)

    @keyword.command(name = "crab", brief = "toggles crabbethew, who already had really rough appearance conditions")
    async def crab(self, ctx, value: bool):
        await self.setValue(ctx, "crab", value)

    @keyword.command(name = "deltarune", brief = "toggles 1/3 response to 'deltarune' in message")
    async def deltarune(self, ctx, value: bool):
        await self.setValue(ctx, "deltarune", value)

    @keyword.command(name = "tetoday", brief = "toggles 1/2 response to 'today' in message")
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

    async def get_falsey_value(self, ctx, member: discord.Member, setting):
        outer = {}
        try:
            with open("settings.json", 'r') as f:
                outer = json.load(f)
                inner = outer.get(str(member.id), {})
                return inner.get(setting, False)
        except FileNotFoundError:
            with open("settings.json", "x") as f:
                outer = {str(member.id): {setting: False}}
                json.dump(outer, f, indent=2)
                print("made a settings file since it wasn't there")
                return False
        except Exception as e:
            print(e)
            print(type(e))
            await ctx.send("something broke, ", str(e))
    async def get_people(self):
        try:
            with open("settings.json", 'r') as f:
                outer = json.load(f)
                return outer.get("dms", [])
        except FileNotFoundError:
                return []
        except Exception as e:
            print(e)
            print(type(e))
            return []

async def setup(bot):
    await bot.add_cog(SetStuff(bot))