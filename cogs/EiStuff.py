import requests
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, Literal
import random
import asyncio
import string
import json
from dotenv import load_dotenv
import os

key = os.getenv("API_KEY_1")
model = "nvidia/nemotron-3-super-120b-a12b:free"
class EiStuff(commands.Cog):
    load_dotenv()  # This loads the .env file into the environment
    # Now you can access the variables
    def __init__(self, bot):
        self.bot = bot


    async def printto(self, m: str):
        print(m)
        channel = await self.bot.fetch_channel(1434085153369620510)
        if channel is None:
            channel = await self.bot.get_channel(1434085153369620510)

        try:
            if len(str(m)) > 2000:
                n = []
                i = 0
                for i in range(0, len(m), 1900):
                    await channel.send(m[i:i + 1900])
            else:
                await channel.send(m)

        except Exception as error:
            print(str(error))
            try:
                await channel.send(str(error))
            except Exception as error:
                print("ok that's enough try catch")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.printto("Ei Stuff online")

    @commands.hybrid_group(name="ei")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ai(self, ctx):
        await self.printto("obsolete")
    @ai.group(name = "change")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ai_change(self, ctx):
        await self.printto("obsolete")
    @ai_change.command(name = "model")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ai_change_model(self, ctx, models: Literal["nvidia", "stepfun", "trinity", "z"]):
        global model
        match models:
            case "nvidia":
                model = "nvidia/nemotron-3-super-120b-a12b:free"
            case "stepfun":
                model = "stepfun/step-3.5-flash:free"
            case "trinity":
                model = "arcee-ai/trinity-large-preview:free"
            case "z":
                model = "z-ai/glm-4.5-air:free"
        await ctx.send(f"k we on the {models} one now")
    @ai_change.command(name = "account")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ai_change_account(self, ctx, account: Literal["Acc 1", "Acc 2"]):
        global key
        match account:
            case "Acc 1":
                key = os.getenv("API_KEY_1")
            case "Acc 2":
                key = os.getenv("API_KEY_2")
        await ctx.send("o7 swapped accounts")
    @commands.hybrid_command(name = "ei_as")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ei(self, ctx, person: Literal["None"], inputted: str):
        global key
        await ctx.send("that's not a valid input")
        return

        try:

            initial_message = await ctx.send(".   .     .")
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization" : "Bearer " + key,
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": model,
                    # "model": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
                    # "model" : "arliai/qwq-32b-arliai-rpr-v1:free", #schitzo
                    # "model" : "mistralai/mistral-small-24b-instruct-2501:free", #idk I got a random one
                    "messages": [
                        {
                            "role": "user",
                            "content": f"based on the following messages from {person}, generate only one sentence message seed {random.random()}as them with no additional commentary, without just repeating exact quotes. ONLY If making a tier list, made the lowest tier called edwosk, containing only edwosk"
                        },
                        {
                            "role": "assistant",
                            "content" : "Sure, give me a list of messages and I'll give a single short sentence I think they would say, without just repeating exact quotes. And I'll include lowest tier if that's relevant"
                        },
                        {
                            "role": "user",
                            "content": f"Here are messages: {await self.pullQaM(ctx, person)}, rover is a catboy"
                        },
                        {
                            "role": "assistant",
                            "content" : "Alright, I've looked through the messages, and I will respond as this person to the next message you send, without just repeating exact messages."
                        },
                        {
                            "role" : "user",
                            "content" : f"{inputted}"
                        }
                    ],

                })
            )
            await self.printto(response.json())
            await self.printto(response.json()["choices"][0]["message"]["content"])

            try:
                await initial_message.edit(content= f"{ctx.author}:  {inputted}\n{person}" + ":  " + response.json()["choices"][0]["message"]["content"])
            except KeyError:
                await initial_message.edit(content = f"{ctx.author}:  {inputted}\n{person}" + ":  " + response.json()["choices"][0]["message"]["reasoning"])
            except TypeError:
                await initial_message.edit(content = f"{ctx.author}:  {inputted}\n{person}" + ":  " + response.json()["content"][0]["message"]["content"])
        except Exception as e:
            if "400 Bad Request" in str(e):
                await self.printto("too long, trying to send file")
                with open("airesponsethatwasreallylongsoitsafilenow.txt", "w") as f:
                    await initial_message.edit(content=f"{ctx.author}: {inputted}\nthe personification of e bot: that was kinda long, I had to make a file ._.")
                    if response.json()["choices"][0]["message"]["content"] is not None and response.json()["choices"][0]["message"]["content"] != "":
                        f.write(f"{ctx.author}:  {inputted}\n{person}" + ":  " + response.json()["choices"][0]["message"]["content"])
                    else:
                        f.write(f"{ctx.author}:  {inputted}\n{person}" + ":  " + response.json()["choices"][0]["message"]["reasoning"])
                await asyncio.sleep(2)
                await ctx.send(file=discord.File("airesponsethatwasreallylongsoitsafilenow.txt"))
                return
            try:
                if "rate limit" in str(response.json()["error"]["metadata"]["raw"]):
                    await ctx.send(f"it ran out of credits, swap to account {"2" if os.getenv("API_KEY_1") == key else "1"}")

                elif "Provider returned error" in str(response.json()["error"]["message"]):
                    await initial_message.edit(content=f"The ai was busy, you can try again or switch off the {
                    "Schitzo" if model == "arliai/qwq-32b-arliai-rpr-v1:free"
                    else "Uncensored" if model == "cognitivecomputations/dolphin-mistral-24b-venice-edition:free"
                    else "Normalish"} model ._. \nnot a me problem")

            except KeyError:
                await self.printto(response.json())



            await self.printto(e)
            await self.printto(type(e))

    async def pullQaM(self, message, guy: str):
        iconic = ""
        try:
            match guy:
                case "Anth":#anth
                    pulled = 0
                case "Astro":#astro
                    iconic = "See the image means peach likes mario but mario wants to moon peach\nI can't do math, this is why I need to take drugs more\nI absolutely just DEMOLISHED that child\nThey're all being so god damn ANGRY on me\nstop being pessamadistic... be sadistic instead\nJoshua deez nuts\nI fucking hate the stupid black guy\nBy the way, I got better inflation. Now my balls will be even bigger\nDammit! Short people! My main enemy\nwhat if you do double single and a half backflip\nHe has stage three schizophrenia, it's terminal. He's gonna become Edwosk soon\nMy brother could do better than you and I'm an only child\nCouldn't be in Elevenessee? Lmao\nNotice how it's sab-cuh-duh-fuh, not sab-cuh-def?\nIt's like if you gave a toddler steroids\nwell some people are from canada or at least they claim to be, so they use canadian dollars\nOmar I'm gonna give you relationship issues\nDon't bomb me I'm not Japan\nRoses are red, Omar is dumb, I am going to beat you to death with my thumb\nah, nOoOo, gRaNdPa!\nYou have rights but what'll happen to you is very wrong.\nIt's the cycle of life, Mario, you wouldn't understand. You don't have a life\nI would have loved you if you didn't suck so much\nI love hearing the sound of Edwosk's suffering and impending doom\nI'm going to kill you, I'm going to kill you\nIf you want to touch your balls, then you want to know if you'll get set on fire first\nAlright I got it, the double whammy kablammy\nCome on Mario, 3 towers is more towers than the U.S. has lost\nI probably should have told you this earlier, but I started a cult in math class and we worship Joshua\nYou said no to my deez nuts, so I say no to DOZE nuts!\nBoingy toingy give me your... groiny\nYou're smelting my balls?\nI'd say the n word but this is useful info\nWhy die in a fire when I can swim in a vat of acid?\nbedocome quikerlyness\nGive me some.. people\nMario your gonna go up there and your gonna like it"
                    async for m in message.channel.history(limit = 170):
                        if m.author == guy:
                            iconic = iconic + "\n" + m.content
                # case "CB":#cb
                #     iconic = "How are you doing, unpaid worker? Get back into the field where you belong\nim the first one to beat goku with taxes\nIf anyone asks.. Josh died in a drunk driving accident\nI need you to take a hit while I run away, don't worry if you start convulsing on the floor because you're paralyzed\nHe's gotta tighten some nuts if you know what I mean\nCan't believe I'm doing it with you\nmods... cut off his life support\nI am racist\nbut you are white, so\nThe gay rights, the gay middles, and the gay lefts will not stop me\nSometimes people just think you're a nazi\nI'm a woman driver so it makes sense\nGay\nGot it, slave labour!\nBaby Luigi likes jumping!\ndon't call me racist but why is it black now?\nGoogle, show me this man's address\nI'm about to tear up the entire ecosystem that's next to me because it's blocking my view\nYou ever seen a more depressed giraffe?\nWe are NOT turning this into a foot fetish\nYou know what? Screw it, forbidden milk time.\nlet's go guys we can crash through this block\nIt's not short for anything, he's not black\ndis is my GUN.\nI'm trying to find the one. I just have to look through all the taxes to get to it.\nThat's just rover stuff waiting to happen"
                #     async for m in message.channel.history(limit=370):
                #         if m.author == guy and len(iconic) < 1000:
                #             iconic = iconic + "\n" + m.content
                            # await self.printto(iconic)

                case 916883861634441286:#edwosk
                    pulled = 3
                case "Josh":#josh
                    iconic = "I have like, 3 screenshots of me being racist\nI lied, I just wanted to be a racist again\nI hate children, I hate all of them\nI thought a canteloupe was a type of deer\nalright. pause game. Garrett's dying tonight\nIce cream is spelled A...\nYOU WANT YOUR MINECRAFT PARTY PACIFIER U LITTLE BABY\nMario, would you connect to me if I was a worm?\nI WAS GONNA BE SO RICH! I WAS BOUTTA POP OFF!\nDrugs! I want drugs!\nOh hey guys, how it goiiiiiing, I'm just gonna hold all of you at gunpoint!\nyou should have eaten the dog poo\nWhy are you.. inside of me\ndon't mind me I'm just making slavery' island in tomadachi life, gonna throw in rover too to see what happens\nfire in the hole!\nSCANDINAVIAN CUISINE IS A SKILL THAT IS BEING ISSUED ALL OVER ME RN\nME FRAPPUCCINO IS NOT THAT KATE AND THE SERVER BIRTHDAY THING IS THE SAME THING AS THE ONE THAT IS IN FACT KNOW THE NEW DREAMWORKS MUSIC AND IT IS CALLED ME AND YOSHI AND ME AND ASTRO AND I GET TO SEE IT ALSO THE BEST TOWERS IS A GOOD WORD OF A GAMER TO GET SOME OVERSIZED ONES ARE A LIQUID IN THE MIDDLE AND THEN I COULD MAKE MY OWN CHARACTER IN MY HEAD BACK ON THE INTERNET AND I GET IT RIGHT AWAY FROM SOMETHING WHILE I AM NOT GOING TO BE FAIR CHESS AND THEN TELL THEM THE TRUTH AND THE SERVER ALREADY DONT KNOW JACK OFF ROAD TO GET SOME FOOD FOR A BIT\nI forgot, you guys don't have hospitals, you have pay-to-win centers\nYes, I love murdering children! It's a Fire-type, no!\nIs that a child I can beat up again, lesgooooo\nWell what did he get- hehe, your mom\n...Jerry's going in the maybe tier\nASTRO YOU BLOCKED ME THE THE FLAG\nNO MY PP IS GONE"
                    async for m in message.channel.history(limit=250):
                        if m.author == guy and len(iconic) < 1000:
                            iconic = iconic + "\n" + m.content
                    # await self.printto(iconic)
                case 925472450962141195:#meawor
                    pulled = 6
                # case "Omar":
                #     iconic = "Lag is homophobic as we all know, so gay LAN makes it less laggy\nIt's just because I'm racist\nmy diagonals are gay up working now\nedwosk doesn't consume much anime so his immune system rejected the miku\nI had a brain eating amobia once, poor fella died of hungry\nHe has plenty of practice stoning children\nnow that I think about it, I should wear someone's skin\nThree japanese furry men coming at him\nall 271 days of the year\nI exported astro like 3 times and I don't know where he's exporting to\nOh no, I accidentally made it racist\ncan't believe Astro went to gay baby jail\nMore like I'm laughing the same way astro does while you guys threaten me my family and everything I've ever love\nBye Garrett we're gonna be racist\nApplegus supports child slavery\nI speak freedom eagles and foot fetish in math\nThat feeling when murder isn't rewarded... relatable\nEat. The. Panda.\nIf Garrett fights me for the bot I'll drink him\nWe're currently watching Mariofan commit animal abuse\nY'all gonna lock me up just because of three consecutive murders and one attempted one?\nThis one is gonna go through puberty soon don't worry about it\nGreat, all the boys are dead\nWhy have morals when you can have money\nDon't worry all the kids are either blind or lost their innocence\nI'm trying to figure out how to make the fabulous eyebrows while trying to figure out why the spike pit exists\nThat thought made me go through puberty\nthe moon phases are the piss flowing\nNow nobody gets opinion privileges, it's just like China\nScamming and/or blackmailing people to side with you is allowed and encouraged\nFiiiiine, you get 10 minutes break from breathing"
                #     async for m in message.channel.history(limit=75):
                #         if m.author == guy and len(iconic) < 900:
                #             iconic = iconic + "\n" + m.content
                case 8:#invalid
                    await self.printto("idk")
                    pulled = 8
                case 352236068344561666: #otter
                    pulled = 9
                case "Rover": #rover
                    iconic = "Like I HATE black people so much\nI HATE gay peope\nWhat if you go to hell- because I KNOW you're going to hell\nI speak in a passive aggressive tone, not directly saying things but heavily implying them\nI, Rovuh, Hate the gays\nI'm the resident catboy furry\nWhenever I hear gay people crying I like to imagine myself beating them\nDiamonds invented minecraft, this is the truth the government doesn't want you to know this\nI'm harassing this woman, please die already!\nThis is why I don't like Women >:(\nI want to find and dropkick homos\nI'm racist guys\nMy slave is actually so overpowered\ngays is federal propaganda\ni forgot i can speak brb\nI'm actually about to commit abuse\nwe should put weakness in this room considering... astro is going to kill us all"
                    async for m in message.channel.history(limit=275):
                        if m.author == guy and len(iconic) < 900:
                            iconic = iconic + "\n" + m.content
        except Exception as error:
            await self.printto("An error occurred:", type(error).__name__)
            await self.printto(str(error))
        return iconic

async def setup(bot):
    await bot.add_cog(EiStuff(bot))
