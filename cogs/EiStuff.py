import requests
import discord
from discord.ext import commands
from typing import Optional
import random
import asyncio
import string
import json

class EiStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ei Stuff online")

    @commands.hybrid_command(name = "testpingai")
    async def ei(self, ctx, guy: discord.Member, inputted: str):
        try:

            initial_message = await ctx.send(".   .     .")
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    # "Authorization": "Bearer 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",
                    # "Authorization": "Bearer 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",
                    "Authorization" : "Bearer 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",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
                    # "model" : "arliai/qwq-32b-arliai-rpr-v1:free", #schitzo
                    "messages": [
                        {
                            "role": "user",
                            "content": f"based on the following messages from {guy.global_name}, generate only one sentence message seed {random.random()}as them with no additional commentary"
                        },
                        {
                            "role": "assistant",
                            "content" : "Sure, give me a list of messages and I'll give a single short sentence I think they would say, only using some of the provided messages"
                        },
                        {
                            "role": "user",
                            "content": f"Here are messages: {await self.pullQaM(ctx, guy)}"
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
            if response.json()["choices"][0]["message"]["reasoning"] is not None and response.json()["choices"][0]["message"]["content"] is not None and 0 < len(response.json()["choices"][0]["message"]["reasoning"]) < len(response.json()["choices"][0]["message"]["content"]):
                await initial_message.edit(content= f"{guy.display_name}" + ":\n" + response.json()["choices"][0]["message"]["reasoning"])
            else:
                await initial_message.edit(content = f"{guy.display_name}" + ":\n" + response.json()["choices"][0]["message"]["content"])
        except Exception as e:
            print(response.json())
            await initial_message.edit(content=f"{type(e)}")
            print(e)
            print(type(e))

    async def pullQaM(self, message, guy: discord.Member):
        iconic = ""
        try:
            match guy.id:
                case 450811106504605706:#anth
                    pulled = 0
                case 770464351336923157:#astro
                    pulled = 1
                case 456858402832908301:#cb
                    iconic = "Ok, time to go jerk off!\nHow are you doing, small child? Get back into the field where you belong\nim the first one to beat goku with unpaid child support bills\nIf anyone asks.. Josh died in a drunk driving accident\nI need you to take a hit while I run away, don't worry if you start convulsing on the floor because you're paralyzed\nHe's gotta tighten some nuts if you know what I mean\nCan't believe I'm doing it with you\nmods... cut off his balls\nthe n word\nbut you are white, so\nQuickly! I gotta look up Among Us roleplay!\nThe gay rights, the gay middles, and the gay lefts will not stop me\nSometimes people just think you're a nazi\nI'm a woman driver so it makes sense\nGay\noh yeah, it does have a hole!\nGot it, slave labour!\nDonkey Kong was riding my ass. You heard me, he got real close\nDang you can screw Luigi?\ndon't call me racist but why is it black now?\nGoogle, show me this man's balls\nI'm about to tear up the entire ecosystem that's next to me because it's blocking my view\nYou ever seen a more depressed giraffe?\nWe are NOT turning this into a foot fetish\nYou know what? Screw it, forbidden milk time.\nyou watched them fuck, I know you did!\nlet's go guys we can cream through this block\nIt's not short for anything, he's not black\ndis is my schlong.\nI'm trying to find the one. I just have to look through all the rule 34 to get to it.\nThat's just furry stuff waiting to happen"
                    async for m in message.channel.history(limit=370):
                        if m.author == guy and len(iconic) < 1000:
                            iconic = iconic + "\n" + m.content
                            print(iconic)

                case 916883861634441286:#edwosk
                    pulled = 3
                case 721389007426158633:#josh
                    pulled = 4
                case 405197452833062912:#mariofan
                    iconic = "Guess he's eating Hitler ¯\\_(ツ)_/¯\nI saw a guy do this in a toothpaste ad once!\nYou know what I do make? Crypto scams\nfire in the hole!\nJosh is like cancer\nCan you beat... your wife.\nI watched you and you just killed yourself\nOh I've got an idea! we recreate 9/11\nastro that joke is dead. Just like Mario and Luigi s father.\nthe tables are encircling the dressers from, behind"
                    async for m in message.channel.history(limit = 170):
                        if m.author == guy:
                            iconic = iconic + "\n" + m.content
                            # print(iconic)
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
