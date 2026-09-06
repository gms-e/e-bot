import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, Literal

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

    @app_commands.allowed_installs(guilds=True, users=True)
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
#
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

    @commands.hybrid_group(name = "operation")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def operation(self, ctx):
        print("obsolete")

    @operation.command(name = "create")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def create(self, ctx, namewithoutoperation: str, category: Literal["Active", "Pending", "Nomar"]):
        if ctx.guild.id != 1086880428650143765:
            await ctx.send("how about you run this in shenanigain central so the bot doesn't fail to make a channel here")
            return
        try:
            category_id = None
            match category:
                case "Active":
                    category_id = 1540006691276464268
                case "Pending":
                    category_id = 1540008214375170198
                case "Completed":
                    category_id = 1540006630022979604
                case "dead":
                    category_id = 1540007625666859029
                case "Nomar":
                    category_id = 1491647429253271563


            category = self.bot.get_channel(category_id)
            if not isinstance(category, discord.CategoryChannel):
                await ctx.send("I messed up the category id oopsie")
                return

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                self.bot.user: discord.PermissionOverwrite(view_channel=True),
                ctx.author: discord.PermissionOverwrite(view_channel=True, pin_messages=True,
                            manage_channels=True, manage_messages=True, bypass_slowmode = True,
                            manage_permissions = True, moderate_members = True)

            }

            # 3. Create the text channel inside the category with the overwrites
            private_channel = await ctx.guild.create_text_channel(
                name=f"operation {namewithoutoperation}",
                category=category,
                overwrites=overwrites
            )


            try:
                with open("channelowners.json", 'r') as f:
                    channelowners = json.load(f)
                    tmp = channelowners.get(str(ctx.author.id), [])
                    tmp.append(private_channel.id)

                    print(tmp)
                    channelowners[str(ctx.author.id)] = tmp
                    print(channelowners)
                    print(f"channelowners: {channelowners}")

                    with open("channelowners.json", 'w') as f:
                        json.dump(channelowners, f, indent=2)

            except FileNotFoundError:
                with open("channelowners.json", "x") as f:
                    tmp = {str(ctx.author.id): [private_channel.id]}
                    json.dump(tmp, f, indent=2)
                    print("made a channelowners file since it wasn't there")
            except Exception as e:
                print(e)
                print(type(e))
                await ctx.send("something broke, ", str(e))
            await ctx.send("o7 made the channel", ephemeral = True)

        except Exception as e:
            print(e)
            print(type(e))

    @operation.command(name="move")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def move(self, ctx, category: Literal["Pending", "Active", "Completed", "Dead", "Nomar"]):
        category_id = None
        match category:
            case "Active":
                category_id = 1540006691276464268
            case "Pending":
                category_id = 1540008214375170198
            case "Completed":
                category_id = 1540006630022979604
            case "Dead":
                category_id = 1540007625666859029
            case "Nomar":
                category_id = 1491647429253271563

        category = self.bot.get_channel(category_id)
        if not isinstance(category, discord.CategoryChannel):
            await ctx.send("I messed up the category id oopsie")
            return

        try:
            with open("channelowners.json", 'r') as f:
                channelowners = json.load(f)
                tmp = channelowners.get(str(ctx.author.id), [])
                if ctx.channel.id in tmp:
                    await ctx.channel.edit(category=category, sync_permissions=False)
                    await ctx.send("wow look this channel and message are in the other category emoji crazy", ephemeral = True)
                else:
                    await ctx.send("imma don't think you can do dat")
                    return

        except Exception as e:
            print(e)
            print(str(e))

    @operation.command(name="invite")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def invite(self, ctx,  channel: discord.TextChannel, people: commands.Greedy[discord.User]):
        try:
            with open("channelowners.json", 'r') as f:
                channelowners = json.load(f)
                tmp = channelowners.get(str(ctx.author.id), [])
                if channel.id in tmp:
                    names = ""
                    for person in people:
                        if person.id == ctx.author.id:
                            await ctx.send("I mean I GUESS you can invite yourself, shouldn't do any harm... y tho")
                        await channel.set_permissions(person, overwrite=discord.PermissionOverwrite(view_channel=True))
                        names = f"{names} {person.name}"
                    await ctx.send(f"o7 {names} got see channel perms", ephemeral = True)
                else:
                    await ctx.send("imma don't think you can do dat")
                    return

        except Exception as e:
            print(e)
            print(str(e))



    @operation.command(name="uninvite")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def uninvite(self, ctx, channel: discord.TextChannel, people: commands.Greedy[discord.User]):
        try:
            with open("channelowners.json", 'r') as f:
                channelowners = json.load(f)
                tmp = channelowners.get(str(ctx.author.id), [])
                if channel.id in tmp:
                    names = ""
                    for person in people:
                        if person.id == ctx.author.id:
                            await ctx.send("funny as it\'d be, I\'d be a bad programmer if I let you ban yourself, so *no.*")
                            continue
                        names = f"{names} {person.name}"
                        await channel.set_permissions(person, overwrite=discord.PermissionOverwrite(view_channel=False))
                    if names:
                        await ctx.send(f"o7 {names} got see channel perms taken", ephemeral=True)

                else:
                    if ctx.author in people:
                        await ctx.send("You don\'t even OWN this channel, why are you trying to ban yourself")
                    else:
                        await ctx.send("imma don't think you can do dat")
                    return

        except Exception as e:
            print(e)
            print(str(e))

    @operation.command(name="setowner")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def setowner(self, ctx, person: discord.User, channels: commands.Greedy[discord.TextChannel]):
        if ctx.author.id != 702906770003198003:
            await ctx.send("what... are you even trying to do.\nit auto sets you as channel owner if you're the one who made it if that's what you\'re worried about")
            return
        overwrites = {
            person: discord.PermissionOverwrite(view_channel=True, pin_messages=True,
                                                    manage_channels=True, manage_messages=True,
                                                    bypass_slowmode=True,
                                                    manage_permissions=True, moderate_members=True)

        }

        try:
            with open("channelowners.json", 'r') as f:
                channelowners = json.load(f)
                for channel in channels:

                    for key, value in channelowners.items():
                        if channel.id in channelowners[key]:
                            channelowners[key].remove(channel.id)

                tmp = channelowners.get(str(person.id), [])
                for channel in channels:
                    tmp.append(channel.id)

                    for target in list(channel.overwrites.keys()):
                        if isinstance(target, discord.Member):
                            # Passing None to overwrite deletes it entirely from the channel
                            await channel.set_permissions(target, overwrite=discord.PermissionOverwrite(pin_messages=False,
                                                manage_channels=False, manage_messages=False,
                                                bypass_slowmode=False,
                                                manage_permissions=False, moderate_members=False))

                    await channel.set_permissions(person, overwrites=overwrites)

                channelowners[str(person.id)] = tmp
                print(channelowners)

                print(f"channelowners: {channelowners}")

                with open("channelowners.json", 'w') as f:
                    json.dump(channelowners, f, indent=2)
                    await ctx.send("o7 that person\'s now the channel owner", ephemeral = True)

        except FileNotFoundError:
            with open("channelowners.json", "x") as f:
                tmp = {str(ctx.author.id): [channel.id]}
                json.dump(tmp, f, indent=2)
                print("made a channelowners file since it wasn't there")
            await ctx.send("o7 that person is now channel owner", ephemeral=True)

        except Exception as e:
            print(e)
            print(str(e))



async def setup(bot):
    await bot.add_cog(SetStuff(bot))