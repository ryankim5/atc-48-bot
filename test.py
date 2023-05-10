import discord
from discord.ext import commands

WELCOME_MESSAGE ="""We have an always running Private Server of PTFS dedicated for semi-realistic ATC roleplay that runs 24/7, 365 days a year. Below is information you may find useful and instructions on how to join ATC 48.

🚀 Our Mission: To ensure that anyone from anywhere in the world can engage in semi-realistic ATC roleplay. With only reasonable barriers and rules in place to safeguard operations from any bad actors.

🛩️ Our Operations: We currently operate one Private Server, with the possibility of adding more in future to cater to demand. All the information you require to get started on your journey here can be found in the category below, with ⁠charts, a ⁠guides and a comprehensive list of ⁠game-rules for you to look at.

**How to join:**
In order to join the game and speak in any of the channels, you must follow these two steps:
1. You must verify using Bloxlink in ⁠bot-commands. Type "/verify" and follow the instructions.
2. You must pass the theory quiz. In order to attempt the quiz, you must be in the server for a minimum of one week. (7 days) The quiz contains questions that assess your knowledge of the rules, and how our operations run. In order to begin the quiz, click the blue button at the bottom of this message.

Once both steps are completed, you will gain access to the game and the rest of the server through the @Members role.


We hope this answered some of your questions, and hope you have a great time here,

**The entire <:smallairplane:1092001686031188018> ATC 48 team.**"""
DISCORD_TOKEN = "MTA5ODgyMjEzMTIwMDA0NTE0Ng.Gumn56.TClzRpANk45nGiFfmEIay_FAozfu4pJgHVgg3A"

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

class Button(discord.ui.Button):
    def __init__(self, label, emoji="✈", style=discord.ButtonStyle.primary):
        self.label, self.emoji, self.style = label, emoji, style
        self.button = discord.ui.button(label=label, style=discord.ButtonStyle.primary, emoji=emoji)

@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    if message.author == bot.user:
        return
    if "apply" in user_message.lower():
        if channel != "game-rules":
            text_channel = bot.get_channel(1091962173791666286)
            await message.channel.send(f"Hello {message.author.mention}, please go to {text_channel.mention} to apply!")
    await bot.process_commands(message)

@bot.command()
async def atc(ctx, airport):
	await ctx.channel.send(f"In testing right now. You requested {airport} right?")

@bot.command()
async def send(ctx):
    await ctx.channel.send(embed = discord.Embed(title="**<:smallairplane:1092001686031188018> Welcome to ATC 48! <:smallairplane:1092001686031188018>**", description=WELCOME_MESSAGE), footer=)

bot.run(DISCORD_TOKEN)