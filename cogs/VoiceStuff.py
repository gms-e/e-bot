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

    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice Stuff online")

    @commands.command()
    async def name(self, ctx):
        print("template")

    # --------------------------------------------jim jam--------------------------------------------------------------#
    @commands.hybrid_group(name="jim", brief="jam - actual command that plays yoshi and me")
    async def jim(self, ctx):
        print("obsolete")
        await ctx.bot.process_commands(ctx)

    @jim.command(name="jam")
    async def jam(self, ctx, count: Optional[int] = commands.parameter(
        displayed_name="song", description="song queue, starts at 0 and goes to 2",default=0),
        censored: Optional[bool] = discord.ext.commands.parameter(displayed_name="beep?", description="beep the name?", default=False)):

        queue = []
        voice_channel = ctx.author.voice.channel

        print(type(censored))
        if "False" in str(censored):
            censored = False
        else:
            censored = True
        print("Censored =", censored)
        if ctx.guild.id != 773015467753209888 or censored:
            print("Censored ver")
            queue = ["music/YoshiAndMePartI-Censored.mp3", "music/YoshiAndMePartII-Censored.mp3",
                     "music/YoshiAndMePartIII-Censored.mp3"]
        else:
            print("Normal ver")
            queue = ["music/YoshiAndMePartI.mp3", "music/YoshiAndMePartII.mp3", "music/YoshiAndMePartIII.mp3"]
            i = 0
            for cue in queue:
                if random.random() < 0.05:
                    que = ["music/YOSHI AND ALT Part I.mp3", "music/YOSHI AND ALT Part II.mp3",
                             "music/YOSHI AND ALT Part III.mp3"]
                    print(f"alt for {i}")
                    queue[i] = que[i]


        if random.random() < 1 / 84:
            await ctx.reply("womp womp, boost debate time", mention_author=False)
            await self.debate(ctx)
            return
        j = 0
        for cue in queue:
            if random.random() < 1 / 100:
               queue[j] = "music/LonkPastBoss.mp3"

        try:
            print(queue[count])
            vc = await self.playSong(ctx, queue[count], count > 2)

        except Exception as error:
            print("An error occurred:", type(error).__name__)

        while count < 3 and voice_channel is not None:
            print(count)

            global stopp
            while vc.is_playing():
                await asyncio.sleep(.1)
                if stopp:
                    print("Stopping...")
                    self.bot.voice_clients[0].stop()
                    print("Stopped")
                    await self.bot.voice_clients.pop().disconnect()
                    print("disconnected")
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
        voice_channel = ctx.author.voice.channel
        song = ""
        if s == "":
            song = "music/boost.mp3"
        else:
            song = s

        if voice_channel is not None:

            vc = await voice_channel.connect(timeout=5)
            await asyncio.sleep(2)
            if random.random() < 1 / 100:
                song = "music/LonkPastBoss.mp3"
                print("lucky link")
            vc.play(discord.FFmpegPCMAudio(song))
            # Sleep while audio is playing.
            print("Built in leave =", quit)
            global stopp
            if quit:
                while vc.is_playing():
                    await asyncio.sleep(.1)
                    if stopp:
                        print("Stopping...")
                        self.bot.voice_clients[0].stop()
                        print("Stopped")
                        await self.bot.voice_clients.pop().disconnect()
                        print("disconnected")
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
        print("obsolete")
        await ctx.bot.process_commands(ctx)

    @boost.command(name="debate")
    async def debate(self, ctx, nada = None):
        print("trying debate")
        await self.playSong(self, ctx, "music/boost.mp3")
        print("worked")
        await self.bot.process_commands(ctx)

#--------------------------------------------command to move people across vc's----------------------------------------#
    # ----------------------------------Bring user to vc--------------------------------------------#
    @commands.hybrid_command(name="kidnap", brief="Kidnaps person to vc")
    async def kidnap(self, ctx, guy: discord.Member = discord.ext.commands.parameter(displayed_name="guy",
                                                                               description="The sucker getting kidnapped (has to be in another vc)")):
        print("kidnapped " + guy.name)
        await ctx.send("This person no longer exists (here)", ephemeral=True)
        await guy.move_to(ctx.author.voice.channel)
        await self.bot.process_commands(ctx)

    #-----------------------------------------------Soundboard person in vc--------------------------------------------#

    @commands.hybrid_command()
    async def soundboard(self, ctx, guy: discord.Member = discord.ext.commands.parameter(displayed_name="guy",
                                                                                   description="Dude you wanna soundboard (must be in vc)")):
        print("soundboarding " + guy.name)
        voice_channel = guy.voice.channel
        print(voice_channel)

        if voice_channel is not None:
            channel = voice_channel.name
            print(channel)
            sound = self.bot.soundboard_sounds[random.randint(0, len(self.bot.soundboard_sounds) - 1)]
            print(self.bot.soundboard_sounds)

            print("picked " + sound.name)

            try:
                vc = await voice_channel.connect()
                await voice_channel.send_sound(sound)
                await ctx.send(sound.name + "ing " + guy.display_name, ephemeral=True)
                await asyncio.sleep(0.3)
                await vc.disconnect()

            except Exception as error:
                print("An error occurred:", type(error).__name__)
                print("gonna try sending as such")
                if "Already connected" in str(error):
                    print("already connected")
                    await ctx.send("DON'T YOU FRICKIN INTERRUPT ME")
                    return
                else:
                    await ctx.send("An error occurred: " + str(error) + "\n I can't frickin use that sound",
                                   ephemeral=True)
                    print("I can't frickin use that sound")
                    self.bot.voice_clients[0].stop()
                    print("Stopped")
                    await self.bot.voice_clients.pop().disconnect()
                    print("disconnected")

async def setup(bot):
    await bot.add_cog(VoiceStuff(bot))