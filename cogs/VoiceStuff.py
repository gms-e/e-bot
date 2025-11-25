import discord
from discord.ext import commands
from typing import Optional
import random
import asyncio
import string

global stopp
stopp = False
class VoiceStuff(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def printto(self, m):
        m = str(m)
        print(m)
        channel = await self.bot.fetch_channel(1434085237914075277)
        if channel is None:
            channel = await self.bot.get_channel(1434085237914075277)

        try:
            print(len(str(m)))
            if len(str(m)) >= 1000:

                n = []
                i = 0
                for i in range(0, len(m), 1000):
                    print(f"correctly found")
                    await channel.send(m[i:i + 1000])
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
        await self.printto("Voice Stuff online")

    @commands.command()
    async def name(self, ctx):
        await self.printto("template")

    # --------------------------------------------jim jam--------------------------------------------------------------#
    @commands.hybrid_group(name="jim", brief="jam - actual command that plays yoshi and me")
    async def jim(self, ctx):
        await self.printto("obsolete")
        await ctx.bot.process_commands(ctx)

    @jim.command(name="jam")
    async def jam(self, ctx, count: Optional[int] = commands.parameter(
        displayed_name="song", description="song queue, starts at 0 and goes to 2",default=0),
        censored: Optional[bool] = discord.ext.commands.parameter(displayed_name="beep?", description="beep the name?", default=False),
                  alt: Optional[bool] = discord.ext.commands.parameter(default=False)):
        usettings = self.bot.get_cog("SetStuff")

        queue = []
        voice_channel = ctx.author.voice.channel

        if "False" in str(censored):
            censored = False
        else:
            censored = True

        if "False" in str(alt):
            alt = False
        else:
            alt = True


        await self.printto(f"Censored = {censored}")
        if ctx.guild.id != 773015467753209888 or censored:
            await self.printto("Censored ver")
            queue = ["music/YoshiAndMePartI-Censored.mp3", "music/YoshiAndMePartII-Censored.mp3",
                     "music/YoshiAndMePartIII-Censored.mp3"]
        else:
            await self.printto("Normal ver")
            queue = ["music/YoshiAndMePartI.mp3", "music/YoshiAndMePartII.mp3", "music/YoshiAndMePartIII.mp3"]
            i = 0

            if alt:
                await self.printto(f"alt = {alt}")
                queue = ["music/YOSHI AND ALT Part I.mp3", "music/YOSHI AND ALT Part II.mp3",
                         "music/YOSHI AND ALT Part III.mp3"]


        if random.random() < 1 / 84 and await usettings.get_value(ctx, ctx.author, "boost"):
            await ctx.reply("womp womp, boost debate time", mention_author=False)
            await self.debate(ctx)
            return
        j = 0
        for cue in queue:
            if random.random() < 1 / 100 and await usettings.get_value(ctx, ctx.author, "boss"):
                await self.printto(f"{j} : {cue} is now lonk")
                queue[j] = "music/LonkPastBoss.mp3"

        try:
            await self.printto(queue[count])
            vc = await self.playSong(ctx, queue[count], count > 2)

        except Exception as error:
            await self.printto("An error occurred:" + str(type(error).__name__))

        while count < 3 and voice_channel is not None:
            await self.printto(count)

            global stopp
            while vc.is_playing():
                await asyncio.sleep(.1)
                if stopp:
                    await self.printto("Stopping...")
                    self.bot.voice_clients[0].stop()
                    await self.printto("Stopped")
                    await self.bot.voice_clients.pop().disconnect()
                    await self.printto("disconnected")
                    stopp = False
                    return

            self.bot.voice_clients[0].stop
            count += 1
            if count < 3 and len(self.bot.voice_clients) > 0:
                self.bot.voice_clients[0].play(discord.FFmpegPCMAudio(source=queue[count]))
        if len(self.bot.voice_clients) > 0:
            await self.bot.voice_clients.pop().disconnect()

        # Delete command after the audio is done playing.
        await self.bot.process_commands(ctx)
#-------------------------------------------stop music helper function--------------------------------------------------#
    async def setStop(self, gBool):
        global stopp
        stopp = gBool
#------------------------------------------Playsong helper method------------------------------------------------------#

    async def playSong(self, ctx, s: string, quit: Optional[bool] = True):
        usettings = self.bot.get_cog("SetStuff")

        voice_channel = ctx.author.voice.channel
        song = ""
        if s == "":
            song = "music/boost.mp3"
        else:
            song = s

        if voice_channel is not None:

            vc = await voice_channel.connect(timeout=5)
            if random.random() < 1 / 100 and await usettings.get_value(ctx, ctx.author, "boss"):
                song = "music/LonkPastBoss.mp3"
                await self.printto("lucky link")
            vc.play(discord.FFmpegPCMAudio(song))
            # Sleep while audio is playing.
            await self.printto(f"Built in leave = {quit}")
            global stopp
            if quit:
                while vc.is_playing():
                    await asyncio.sleep(.1)
                    if stopp:
                        await self.printto("Stopping...")
                        self.bot.voice_clients[0].stop()
                        await self.printto("Stopped")
                        await self.bot.voice_clients.pop().disconnect()
                        await self.printto("disconnected")
                        stopp = False
                        return
                await vc.disconnect()
                await vc.leave()
            else:
                return vc

        # Delete command after the audio is done playing.
        await ctx.message.delete()

#----------------------------------------Actual boost debate command that NOBODY uses----------------------------------#
    @commands.hybrid_group(name="boost", brief="debate")
    async def boost(self, ctx):
        await self.printto("obsolete")
        await ctx.bot.process_commands(ctx)

    @boost.command(name="debate")
    async def debate(self, ctx):
        await self.printto("trying debate")
        try:
            await self.playSong(ctx,"music/boost.mp3", True)
        except Exception as error:
            await self.printto(f"An error occurred: {type(error).__name__}")
            await self.printto(str(error))
        await self.printto("worked")
        await self.bot.process_commands(ctx)

#--------------------------------------------super censored song----------------------------------------#
    @commands.hybrid_command(name="chinasong")
    async def chinasong(self, ctx):
        try:
            await ctx.send("||o7||")
            await self.playSong(ctx, 'music/__ and _.mp3', True)
        except Exception as error:
            await self.printto(f"An error occurred: {type(error).__name__}")
            await self.printto(str(error))
    # ----------------------------------Bring user to vc--------------------------------------------#
    @commands.hybrid_command(name="kidnap", brief="Kidnaps person to vc")
    async def kidnap(self, ctx, guy: discord.Member = discord.ext.commands.parameter(displayed_name="guy",
                                                                               description="The sucker getting kidnapped (has to be in another vc)")):
        await self.printto(f"kidnapped {guy.name}")
        await ctx.send("This person no longer exists (here)", ephemeral=True)
        await guy.move_to(ctx.author.voice.channel)
        await self.bot.process_commands(ctx)

    #-----------------------------------------------Soundboard person in vc--------------------------------------------#

    @commands.hybrid_command()
    async def soundboard(self, ctx, guy: discord.Member = discord.ext.commands.parameter(displayed_name="guy",
                                                                                   description="Dude you wanna soundboard (must be in vc)")):
        await self.sendSound(ctx, guy, False)

    async def sendSound(self, ctx, guy, redo):
        await self.printto(f"soundboarding {guy.name}")
        voice_channel = guy.voice.channel
        await self.printto(voice_channel)

        if voice_channel is not None:
            channel = voice_channel.name
            await self.printto(channel)
            sound = self.bot.soundboard_sounds[random.randint(0, len(self.bot.soundboard_sounds) - 1)]
            # await self.printto(self.bot.soundboard_sounds)

            await self.printto(f"picked {sound.name}")

            try:
                if not redo:
                    vc = await voice_channel.connect()
                await voice_channel.send_sound(sound)
                await ctx.send(sound.name + "ing " + guy.display_name, ephemeral=True)
                await asyncio.sleep(0.3)
                await vc.disconnect()

            except Exception as error:
                await self.printto(f"An error occurred: {type(error).__name__}")
                if "Already connected" in str(error) and not redo:
                    await self.printto("already connected")
                    await ctx.send("DON'T YOU FRICKIN INTERRUPT ME")
                    return
                elif redo:
                    self.bot.voice_clients[0].stop()
                    await self.bot.voice_clients.pop().disconnect()
                else:
                    await ctx.send("An error occurred: " + str(error) + "\n I can't frickin use that sound",
                                   ephemeral=True)
                    await self.sendSound(ctx, guy, True)
                    await self.printto("I can't frickin use that sound")
                    self.bot.voice_clients[0].stop()
                    await self.printto("Stopped")
                    await self.bot.voice_clients.pop().disconnect()
                    await self.printto("disconnected")

async def setup(bot):
    await bot.add_cog(VoiceStuff(bot))