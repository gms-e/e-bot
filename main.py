import json
import string
from argparse import BooleanOptionalAction
import discord
from discord.ext import commands, tasks
import asyncio
# import interactions
import logging
from dotenv import load_dotenv
import os
from discord import app_commands
from typing import Optional
import random
import ffmpeg
import datetime
import subprocess
load_dotenv()



token = os.getenv("DISCORD_TOKEN")#you're not getting my bot token that easy

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.voice_states = True
intents.presences = True
intents.moderation = True
intents.webhooks = True
#slashClient = discord.Client(intents=intents)#slash command
bot = commands.AutoShardedBot(command_prefix=["e, ", "E, ", ",e ", ",E ", "jarvis, ", "mods, ", "e "], intents=intents)
messageCount = 0
#----------------------------------slash command stuff ----------------------------------------------#
#@bot.event
#async def on_ready():
#    print("tree ready!")
async def printto(m: str):
    print(m)
    channel = await bot.fetch_channel(1434085056393252904)
    if channel is None:
        channel = await bot.get_channel(1434085056393252904)

    try:
        await channel.send(m)
    except Exception as error:
        print(str(error))
        try:
            await channel.send(str(error))
        except Exception as error:
            print("ok that's enough try catch")

@bot.event
async def on_ready():


    await printto(f'{bot.user} has connected to Discord! Version {discord.__version__}')
    try:
        synced = await bot.tree.sync()
#     try:
#         await timechecks.start()
#     except Exception as error:
#         await printto(error)
#         await printto(str(error))
        await printto(f"bot ready")
    except Exception as e:
        print(e)
        print(type(e))
#
# # @tasks.loop(minutes=30) # Runs every 60 seconds (adjust as needed)
# async def timechecks():
#     checker = bot.get_cog("PrintStuff")
#
#     servNum = -1
#     try:
#         with open("serverStat.txt", 'r') as f:
#             line = f.readline()
#             servNum = int(line.strip())  # Strip whitespace and convert to int
#     except FileNotFoundError:
#         with open("serverStat.txt", "x") as f:
#             f.write("0")
#             await printto("made a file since it wasn't there, running as if was offline")
#
#     if await checker.sup() == 1 and servNum <= 0:
#         await printto("server up and used to be offline")
#         with open("serverStat.txt", "w") as f:
#             f.write("1")
#         await bot.get_channel(1264704750633619486).send("<@&1426289745784340591> server people,\nServer up")
#     elif await checker.sup() == 1 and servNum == 1:
#         await printto("server up and used to be online")
#     else:
#         await printto("Server not up")
#         with open("serverStat.txt", "w") as f:
#             f.write("0")

        #TODO: add warndle, a warning for the last 30 min of the day IF nobody's done the wordle yet



############################stolen because I'm not paid######################

def capi_sentence(sentence):
    global messageCount
    shut = False
    if "e, shut up" in sentence:
        shut = True

    new_sentence = ""
    number = 0  # Dummy number for tracking

    for letter in sentence.lower():
        if len(new_sentence) < 2:  # Creates the first two letter
            random_number = random.randint(0, 1)  # This randomly decides if the letter should be upper or lowercase
            if random_number == 0:
                new_sentence += letter.upper()
            else:
                new_sentence += letter
        else:
            if (new_sentence[number - 2].isupper() and new_sentence[number - 1].isupper() or new_sentence[
                number - 2].islower() and new_sentence[number - 1].islower()) == True:
                # Checks if the two letters before are both upper or lowercase
                if new_sentence[number - 1].isupper():  # Makes the next letter the opposite of the letter before
                    new_sentence += letter.lower()
                else:
                    new_sentence += letter.upper()
            else:
                random_number = random.randint(0, 1)
                if random_number == 0:
                    new_sentence += letter.upper()
                else:
                    new_sentence += letter

        number += 1  # Add one more to the tracking
    if shut:
        new_sentence = new_sentence[:len(new_sentence)//2] + " Oh wait I gotta shut up now"
        messageCount = 1
        print(messageCount)
    return(new_sentence)

##############################################################################
stopwait = False
mocks = ["https://tenor.com/view/luigi-coo-coo-crazy-luigis-mansion-dark-moon-gif-1213275346224547321", "bro posted a stupid link like a stupid nerd stupid idiot dunderhead", "\"link deez nuts wif yo mouth\". -Mariofan", "imagine posting a link", "bro posted a link", "shut up"]
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with (bot):
        await load()
        await bot.start(token)#, log_handler=handler, log_level=logging.DEBUG)
        await bot.tree.sync()  # guild=discord.Object(id=Your guild id))



@bot.event
async def on_message(message):
    usettings = bot.get_cog("SetStuff")
    if message.author == bot.user:
        # try:
        #     m = await message.channel.fetch_message(message.id)
        #     await m.edit(content=message.content.replace("h", "**e**"))
        #     await m.edit(content=message.content.replace("H", "**E**"))
        # except Exception as error:
        #     await printto(error)
        return
    lower = message.content.lower()
#----------------------------------Kys catcher--------------------------------------------#

    # await ctx.author.add_roles()
    try:

        if ("kys" in lower or "kill yourself" in lower) and await usettings.get_value(message, message.author, "kys"):

            await printto(f"saw kys")
            await message.add_reaction("🇪")
            await message.add_reaction("<:kyours:1377804377540137010>")
            return
    except Exception as error:
        await printto(error)
        await printto(str(error))

# -----------------------------Omar anim catcher------------------------------------------#
    if "omar" in lower and await usettings.get_value(message, message.author, "omaranim"):
        if "animate" in lower or "animation" in lower or "animating" in lower:
            await message.reply("shut up, I'm a cooler project", mention_author=False)
            await message.add_reaction("<:ughmar:1307892558063468606>")

# -----------------------------Skill issue catcher------------------------------------------#

    if ("skill issue" in lower or "too hard"  in lower or "died"  in lower) and await usettings.get_value(message, message.author, "skillissue"):

        await printto(f"saw skill issue")
        await message.add_reaction("🇪")
        await message.add_reaction("<:skillissue:1120782165483978802>")
        # await message.add_reaction("<1377804377540137010>")
        return

    # ----------------------------------Ohh Canadaa--------------------------------------------#
    if message.author.id == 405197452833062912 and message.channel.name == "monoday-chat":
        await printto(f"Racist time")
        await message.add_reaction("🇨🇦")
    # ----------------------------------so sad catcher--------------------------------------------#
    if "so sad" in lower and "play" not in lower and "." not in lower:
        await printto("found so sad")

        if await usettings.get_value(message, message.author, "sadeyes"):
            await message.add_reaction("🇪")
            await message.add_reaction("<:sosad:1445204195832500396>")

        if random.random() < 0.01 * (5/5) and await usettings.get_value(message, message.author, "sosad"):
            await printto("HOW SAD???")
            if random.random() < 0.5:
                await message.channel.send(file=discord.File("how sad.png"))
            else:
                await message.channel.send(file=discord.File("erg.png"))
            await asyncio.sleep(20)
            voices = bot.get_cog("VoiceStuff")
            await voices.jam(message, 0)

    #----------------------------------Stupid o clock enforcer-------------------------------------------#

    if message.channel.id == 873640967138336768 and discord.utils.get(message.guild.roles, name="timed worse than Omar") in message.author.roles:
        pacific = discord.utils.get(message.guild.roles, name="Pacific Time -8")
        central = discord.utils.get(message.guild.roles, name="Central Time -6")
        eastern = discord.utils.get(message.guild.roles, name="Eastern Time -5")
        mountain = discord.utils.get(message.guild.roles, name="Mountain Time -7")
        ceneuro = discord.utils.get(message.guild.roles, name="Central European Time +1")

        t = datetime.datetime.now().hour
        if pacific in message.author.roles:
            if t > 6 or t < 0:
                await message.delete()
                await message.author.send("oi")
        elif central in message.author.roles:
            if t > 8 or t < 2:
                await message.delete()
                await message.author.send("oi")
        elif eastern in message.author.roles:
            if t > 9 or t < 3:
                await message.delete()
                await message.author.send("oi")
        elif mountain in message.author.roles:
            if t > 7 or t < 1:
                await message.delete()
                await message.author.send("oi")
        elif ceneuro in message.author.roles:
            if t > 8 or t < 2:
                await message.delete()
                await message.author.send("oi")

    #------------------------------------krusty krab------------------------------------------------------#
    if "cr" in message.content and "a" in message.content and "b" in message.content and "i" not in message.content and "o" not in message.content and "h" not in message.content and await usettings.get_value(message, message.author, "crab"):
        await message.channel.send(file=discord.File("crabbethy.jpg"))
    #----------------------------------Plays yosh when phrase--------------------------------------------#
    if "play yoshi and me" in lower and await usettings.get_value(message, message.author, "yoshiandme"):
        await printto("saw yosh")
        voices = bot.get_cog("VoiceStuff")
        if "e," not in lower and "." in lower and "so sad" in lower:
            await printto("prankd")
            await voices.playSong(message, "music/Yoshi and nah.mp3")
        elif "censor" in lower or "beep" in lower or "less" in lower:
            await printto("saw censored in yosh")
            await voices.jam(message, 0, True)
        else:
            await printto("norm yosh time")
            await voices.jam(message, 0)
    #------------------------------------Plays boost when phrase-------------------------------------------#
    if "boost" in lower and "debate" in lower and "play" in lower and await usettings.get_value(message, message.author, "boost"):
        voices = bot.get_cog("VoiceStuff")
        await voices.debate(message)

    # if ("world" in lower or "server" in lower) and ("custody" in lower or "mine" in lower) and await usettings.get_value(message, message.author, "worldismine"):
    #     voices = bot.get_cog("VoiceStuff")
    #     await voices.playSong(message, "music/World is Mine - Kasane Teto (Synthesizer V Cover) [0eaeiSjh7pU].mp3")
    #-----------------------------------Stop music command------------------------------------------------#
    if "e, shut up" in lower and await usettings.get_value(message, message.author, "leavevc"): #removed "good" "music" req bc deadline
        await printto("saw stop command")
        voices = bot.get_cog("VoiceStuff")
        await voices.setStop(True)
    #----------------------------------Random mock chance--------------------------------------------#
    global messageCount
    if random.random() < 1/1000  and await usettings.get_value(message, message.author, "mock"):
        messageCount = 1
        await printto("Wow, you're so LUCKY")

    #-----------------------------------TTSn't------------------------------------------------------#
    if random.random() < 1/500 and ",join" in message.content and await usettings.get_value(message, message.author, "fakejoin"):
        voices = bot.get_cog("VoiceStuff")
        await voices.soundboard(message.author)
    #-------------------------------------Deltarune tomorrow---------------------------------------------#
    if random.random() < 1/3 and await usettings.get_value(message, message.author, "deltarune"):
        if "deltarune" in lower or "delta rune" in lower:
            if "tomorrow" not in lower:
                await message.reply("deltarune tomorrow", mention_author=False)
            else:
                await message.reply("deltarune tomorrow :D", mention_author=False)
            await printto("deltarune tomorrow")


    #----------------------------------respond to pings--------------------------------------------#
    # if  await usettings.get_value(message, message.author, "replyeyes") and bot.user.mentioned_in(message):
    #     await message.add_reaction("👀")
        #------------------Calls mock when mock count over 0 and not escaped------------------------------#
    elif messageCount > 0 and message.author != bot.user and not "_ _" in message.content:
        if "https" in message.content:
            await message.reply(mocks[random.randint(0, len(mocks)-1)], mention_author=False)
        else:
            await message.reply("\"" + capi_sentence(message.content) + "\"", mention_author=False)
        messageCount -= 1
        await printto(messageCount)

    await bot.process_commands(message)

tts = 0




#-------------------------------------------Marle reactions---------------------------------------------------------#
marle = ["<:CircleFairy:1400643761528111105>", "<:Parlor:1400314790232199248>", "<:Sunnyside:1400314751074041916>",
         "<:Shell:1400314727762231313>", "<:Fire:1400314711077027840>", "<:Marle:1400314691586101309>",
         "<:Lustful:1400314677782642809>", "<:Marlet:1400314659919364196>", "<:Devout:1400314645939617852>",
         "<:Merger:1400314629829427301>", "<:Chord:1400314610137169950>", "<:Miku:1400314592051331132>",
         "<:Ghost:1400314573013389363>", "<:Lover:1400314395665371287>", "<:Inkling:1400314383376191598>",
         "<:Interviewer:1400314369631457370>", "<:Astronaut:1400314286147899482>", "<:Farmhand:1400314265595936891>",
         "<:Birdbrain:1400314248726577313>", "<:ANTIMARLE:1400314229940031538>", "<:Popper:1400314215536922766>",
         "<:Windy:1400314202740232355>","<:Mystery:1400314188269621368>", "<:Elephant:1400314177331134564>",
         "<:Broker:1400314165389820017>","<:MarleFan:1400314149103472711>", "<:Insomniac:1400314126026281051>",
         "<:Ohmar:1400314114609381416>","<:Bargain:1400314095747465218>", "<:Canadian:1400643436243325060>",
         "<:Booster:1400314039820746902>","<:Santa:1400314008413802556>", "<:Pride:1400313975731912755>",
         "<:Cafe:1400313952562450502>","<:Yoshee:1400313943075065866>", "<:Dresser:1400313930831630396>",
         "<:Pastel:1400313919192563743>","<:Partygoer:1400313906106466356>", "<:Hater:1400313891157835817>",
         "<:Spooky:1400313880617553960>","<:Drill:1400313870341505225>", "<:Host:1400313859817996420>",
         "<:CB:1400313849298550896>","<:Bubble:1400313836623495188>", "<:Wiki:1400313825735086081>",
         "<:Spacey:1400313811705270322>","<:Technician:1400313794944827513>"]

# @bot.tree.context_menu(name = "Random Marle Message")
# @app_commands.allowed_installs(guilds=True, users=False)
# @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
# async def reactMarle(interaction: discord.Interaction, message: discord.Message):
#     cmarle = marle[random.randint(0, len(marle) - 1)]
#     await printto(cmarle, interaction.user.name)
#     await message.add_reaction(cmarle)
#     await interaction.response.send_message(f"{cmarle}'d it.", ephemeral=True)



@bot.tree.context_menu(name = "Marle Message With")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def dropMarle(interaction: discord.Interaction, message: discord.Message):
    rcount = 0

    async def cb(self, interaction: discord.Interaction):
        # Handle the user's selection here
        selected_value = self.values[0]  # For single-selection
        await printto(f"{selected_value} from {interaction.user}")
        await message.add_reaction(selected_value)
        nonlocal rcount
        rcount += 1
        await interaction.response.edit_message(
            content=f"You can do more than {rcount} if ya want, nobody's looking. \n(Except console👀.)")
        await interaction.followup.send_message(f"{selected_value}'d it.", ephemeral=True)


    class MySelect(discord.ui.Select):
        def __init__(self):
            options = []
            limit = 0
            for m in marle:
                if limit<24:
                    options.append(discord.SelectOption(label=m.split(":")[1], value = m, emoji = m))

                limit += 1
            super().__init__(placeholder="Choose a Marle...", options=options, custom_id = "First")
        callback = cb


    class MySeclect(discord.ui.Select):
        def __init__(self):
            optwons = []
            limit = 0
            for m in marle:
                if limit > 24:
                    optwons.append(discord.SelectOption(label=m.split(":")[1], value=m, emoji=m))
                limit += 1
            super().__init__(placeholder="Choose a Marle...", options=optwons, custom_id = "Second")
        callback = cb


    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(MySelect())
            self.add_item(MySeclect())
    try:
        await interaction.response.send_message(f"Pick yer marle, ANY marle", view=MyView(), ephemeral=True)
    except Exception as error:
        await printto(error)
        await printto(str(error))


@bot.tree.context_menu(name="killing you")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def killtarget(inter: discord.Interaction, mes: discord.Message):
    parser = bot.get_cog("PrintStuff")
    try:
        leftcat = await parser.parseleftcat(inter.user.id)
        rightcat = await parser.parserightcat(mes.author.name)
        await parser.genfetchedcat(leftcat, rightcat, inter.user, mes.author, inter)

    except Exception as error:
        await printto(error)
        await printto(str(error))


@bot.tree.context_menu(name="trackiller")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def killtracker(inter: discord.Interaction, message: discord.Message):
    try:
        if "https://" in message.content and "?si=" in message.content:
            time = ""
            if "&t=" in message.content:
                time = message.content[message.content.index("&t="):]
                if " " in time:
                    time = time[:time.index(" ")]
                if "\n" in time:
                    time = time[:time.index(" ")]
            bettermessage = message.content[:message.content.index("?si=")]
            bettermessage = bettermessage[bettermessage.index("https://"):]
            bettermessage = bettermessage + time
            await inter.response.send_message(bettermessage, file = discord.File("images/trackiller.png"))
        elif "https://" in message.content and "?si=" not in message.content:
            await inter.response.send_message("there isn't a tracker as far as I can tell my guy.", ephemeral=True)
        else:
            await inter.response.send_message("Is there even a *link* in there?? not that I can tell\n._.", ephemeral=True)
    except Exception as e:
        print(e)



@bot.tree.context_menu(name = "Collect Anth")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def canpthure(interaction: discord.Interaction, message: discord.Message):
    try:
        chanthnel = await bot.fetch_channel(1529322436741566526)
        await chanthnel.send(f"-# {interaction.user.name} got an anth:")
        await chanthnel.send(str(message.author.avatar.url))
        await interaction.response.send_message("Anth Collected!", ephemeral=True)
    except Exception as e:
        print(e)




#---------------------------------command to reboot pc, for omar's eyes only----------------------------#

@bot.hybrid_command(brief="Reboots the entire pc (for remote updating)")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def sudoreboot(ctx, password, secondpassword):
    if ctx.author.id != 702906770003198003:
        await ctx.send("-. -\nno. You're not me.")
        return
    second = os.getenv("SECOND")
    if int(second) != int(secondpassword):
        await ctx.send("ain't no way you forgot THAT password")
        return

    await ctx.send("goodbye world")
    subprocess.run(["sudo", "-S", "reboot"], input=f"{password}\n", text=True)


#----------------------------------Mocks message used on--------------------------------------------#
@bot.tree.context_menu(name = "mock this")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def this(interaction: discord.Interaction, message: discord.Message):

    await printto("mocking this:")
    if "http" in message.content:
        await message.reply(mocks[random.randint(0, len(mocks)-1)], mention_author=False)
    else:
        await message.reply("\"" + capi_sentence(message.content) + "\"", mention_author=False)
    await interaction.response.send_message("k", ephemeral=True)
#-------------------------------------------------------------Mock branches--------------------------------------------#
@bot.hybrid_group(brief = "next | this(app menu)")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def mock(ctx):
   await printto("obsolete")

@mock.command(brief="Mocks specified amount of future messages")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def next(ctx,  number: Optional[int] = None):
    await printto("mocking next " + str(number))
    global messageCount
    await printto(messageCount)
    if 16 > number > -1 and messageCount <= 0:  # apparantly if two people use -1 at once it overflows, so <=0 it is
        await printto(f"saw {number}")
        await printto(ctx.message.author)
        messageCount = number
        await ctx.send(f"o7 on it", ephemeral=True)
    elif messageCount > 0:
        await ctx.send(f"skill issue, mocking still at {messageCount}")
        return

    await bot.process_commands(ctx)

# #----------------------------------Mocks user who was pinged--------------------------------------------#
# @mock.command(name = "that", brief = "Mocks last message of given user")
# async def that(ctx, guy: discord.User):
#     #await printto("mockprev")
#     words = ctx.history(limit = 20, oldest_first = False)
#
#     #await ctx.channel.last_message.reply("e")god, getting the user pinged was SO HARD for literally no reason
#     await printto(words)
#     #await printto(f"assigned fetched message")
#
#     foundMessage = False
#     mockee = None
#     async for message in words:
#         if message.author == guy and not foundMessage:
#             await printto(message)
#             mockee = message
#             foundMessage = True
#
#     await mockee.reply("\"" + capi_sentence(mockee.content) + "\"", mention_author=False)
#     await ctx.send(f"k", ephemeral=True)
#
#     await printto("mocking")
#     await bot.process_commands(ctx)


asyncio.run(main())#, log_handler=handler, log_level=logging.DEBUG)
#bot.run(token, log_handler=handler, log_level=logging.DEBUG)
