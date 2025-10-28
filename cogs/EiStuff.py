import requests
import discord
from discord.ext import commands
from typing import Optional, Literal
import random
import asyncio
import string
import json
from dotenv import load_dotenv
import os

class EiStuff(commands.Cog):
    load_dotenv()  # This loads the .env file into the environment
    # Now you can access the variables
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ei Stuff online")
    @commands.hybrid_command(name = "testpingai")
    async def ei(self, ctx, person: Literal["Astro", "CB"], inputted: str):
        API_KEY_1 = os.getenv("API_KEY_1")
        try:

            initial_message = await ctx.send(".   .     .")
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization" : "Bearer " + API_KEY_1,
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    # "model": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
                    "model" : "arliai/qwq-32b-arliai-rpr-v1:free", #schitzo
                    "messages": [
                        {
                            "role": "user",
                            "content": f"based on the following messages from {person}, generate only one sentence message seed {random.random()}as them with no additional commentary"
                        },
                        {
                            "role": "assistant",
                            "content" : "Sure, give me a list of messages and I'll give a single short sentence I think they would say, only using some of the provided messages"
                        },
                        {
                            "role": "user",
                            "content": f"Here are messages: {await self.pullQaM(ctx, person)}"
                        },
                        {
                            "role": "assistant",
                            "content" : "Alright, I've looked through the messages, and I will respond as this person to the next message you send."
                        },
                        {
                            "role" : "user",
                            "content" : f"{inputted}"
                        }
                    ],

                })
            )
            print(response.json())
            print(response.json()["choices"][0]["message"]["content"])
            try:
                await initial_message.edit(content= f"{ctx.author}:  {inputted}\n{person}" + ":  " + response.json()["choices"][0]["message"]["content"])
            except KeyError:
                await initial_message.edit(content = f"{ctx.author}:  {inputted}\n{person}" + ":  " + response.json()["choices"][0]["message"]["reasoning"])
            except TypeError:
                await initial_message.edit(content = f"{ctx.author}:  {inputted}\n{person}" + ":  " + response.json()["content"][0]["message"]["content"])
        except Exception as e:
            print(response.json())
            await initial_message.edit(content=f"{type(e)}\n{str(e)}")
            print(e)
            print(type(e))

    async def pullQaM(self, message, guy: str):
        iconic = ""
        try:
            match guy:
                case "Anth":#anth
                    pulled = 0
                case "Astro":#astro
                    iconic = "See the image means peach likes mario but mario wants to moon peach\nI can't do math, this is why I need to take drugs more\nI absolutely just DEMOLISHED that child\nThey're all being so god damn HORNY on me\nstop being pessamadistic... be sadistic instead\nJoshua deez nuts\nI fucking hate the stupid black guy\nBy the way, I got better inflation. Now my balls will be even bigger\nDammit! Short people! My main enemy\nwhat if you do double single and a half backflip\nHe has stage three schizophrenia, it's terminal. He's gonna become Edwosk soon\nMy brother could do better than you and I'm an only child\nCouldn't be in Elevenessee? Lmao\nNotice how it's sab-cuh-duh-fuh, not sab-cuh-def?\nIt's like if you gave a toddler steroids\nwell some people are from canada or at least they claim to be, so they use canadian dollars\nOmar I'm gonna give you relationship issues\nDon't bomb me I'm not Japan\nRoses are red, Omar is dumb, I am going to beat you to death with my thumb\nah, nOoOo, gRaNdPa!\nYou have rights but what'll happen to you is very wrong.\nIt's the cycle of life, Mario, you wouldn't understand. You don't have a life\nI would have loved you if you didn't suck so much\nI love hearing the sound of Edwosk's suffering and impending doom\nI'm going to touch you, I'm going to touch you\nIf you want to touch your balls, then you want to know if you'll get set on fire first\nAlright I got it, the double whammy kablammy\nCome on Mario, 3 towers is more towers than the U.S. has lost\nI probably should have told you this earlier, but I started a cult in math class and we worship Joshua\nYou said no to my deez nuts, so I say no to DOZE nuts!\nBoingy toingy give me your... groiny\nIf I'm awake then I'll bone with you\nYou're smelting my balls?\nI'd say the n word but this is useful info\nWhy die in a fire when I can swim in a vat of acid?\nbedocome quikerlyness\nGive me some.. people\nMario your gonna go up there and your gonna like it"
                    async for m in message.channel.history(limit = 170):
                        if m.author == guy:
                            iconic = iconic + "\n" + m.content
                case "CB":#cb
                    iconic = "Ok, time to go jerk off!\nHow are you doing, small child? Get back into the field where you belong\nim the first one to beat goku with unpaid child support bills\nIf anyone asks.. Josh died in a drunk driving accident\nI need you to take a hit while I run away, don't worry if you start convulsing on the floor because you're paralyzed\nHe's gotta tighten some nuts if you know what I mean\nCan't believe I'm doing it with you\nmods... cut off his balls\nthe n word\nbut you are white, so\nQuickly! I gotta look up Among Us roleplay!\nThe gay rights, the gay middles, and the gay lefts will not stop me\nSometimes people just think you're a nazi\nI'm a woman driver so it makes sense\nGay\noh yeah, it does have a hole!\nGot it, slave labour!\nDonkey Kong was riding my ass. You heard me, he got real close\nDang you can screw Luigi?\ndon't call me racist but why is it black now?\nGoogle, show me this man's balls\nI'm about to tear up the entire ecosystem that's next to me because it's blocking my view\nYou ever seen a more depressed giraffe?\nWe are NOT turning this into a foot fetish\nYou know what? Screw it, forbidden milk time.\nyou watched them fuck, I know you did!\nlet's go guys we can cream through this block\nIt's not short for anything, he's not black\ndis is my schlong.\nI'm trying to find the one. I just have to look through all the rule 34 to get to it.\nThat's just furry stuff waiting to happen"
                    async for m in message.channel.history(limit=370):
                        if m.author == guy and len(iconic) < 1000:
                            iconic = iconic + "\n" + m.content
                            print(iconic)

                case 916883861634441286:#edwosk
                    pulled = 3
                case 721389007426158633:#josh
                    pulled = 4
                #case :#mf
                    #no.
                case 925472450962141195:#meawor
                    pulled = 6
                case 702906770003198003:#om
                    pulled = 7
                case 8:#invalid
                    print("idk")
                    pulled = 8
                case 352236068344561666: #otter
                    pulled = 9
                case 617347174120030208: #rover
                    pulled = 10
        except Exception as error:
            print("An error occurred:", type(error).__name__)
            print(str(error))
        return iconic

async def setup(bot):
    await bot.add_cog(EiStuff(bot))
