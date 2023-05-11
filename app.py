import discord
from discord.ext import commands

AIRPORT_SELECT = [
"[IGAR] Air Base Garry",
"[IJAF] Al Najaf",
"[IBAR] Barra Airport",
"[IBLT] Boltic Airfield",
"[IGRV] Grindavik Airport",
"[IRFD] Greater Rockford",
"[IHEN] Henstridge Airfield",
"[HMS] HMS Queen Elizabeth II",
"[IZOL] Izolirani Intl.",
"[ILAR] Larnca Intl.",
"[ILKL] Lukla Airport",
"[IMLR] Mellor Intl.",
"[IPAP] Paphos Intl.",
"[IPPH] Perth Intl.",
"[ISCM] RAF Scampton",
"[IDCS] Saba Airport",
"[IBTH] Saint Barthelemy",
"[ISAU] Sauthamptona",
"[ISKP] Skopelos Airfield",
"[ITKO] Tokyo Intl.",
"[ITRC] Training Centre",
"[USS] USS Gerald R. Ford"
]

AIRPORT_NAMES = [
"airbase_garry",
"al_najaf",
"barra",
"boltic",
"cyprus",
"grindavik"
"henstridge",
"izolirani",
"izolirani_ground",
"larnaca",
"larnaca_ground",
"lukla",
"mellor",
"paphos",
"perth",
"perth_ground",
"raf_scampton",
"rockford",
"rockford_Ground",
"saba",
"saint_barthelemy",
"sauthamptona",
"skopelos",
"toyko",
"tokyo_ground",
"traning_centre"]

# Airport ATC Statuses, in this format:
# User, ATIS
atc_status = {
"airbase_garry" : [False, False],
"al_najaf" : [False, False],
"barra" : [False, False],
"boltic" : [False, False],
"cyprus" : [False, False],
"grindavik" : [False, False],
"henstridge" : [False, False],
"izolirani" : [False, False],
"izolirani_ground" : [False, False],
"larnaca" : [False, False],
"larnaca_Ground" : [False, False],
"lukla" : [False, False],
"mellor" : [False, False],
"paphos" : [False, False],
"perth" : [False, False],
"perth_Ground" : [False, False],
"raf_scampton" : [False, False],
"rockford" : [False, False],
"rockford_Ground" : [False, False],
"saba" : [False, False],
"saint_barthelemy" : [False, False],
"sauthamptona" : [False, False],
"skopelos" : [False, False],
"toyko" : [False, False],
"tokyo_Ground" : [False, False],
"traning_centre" : [False, False],
}

# Token 
TOKEN = "NONE"

# Intents and Bot
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Guild
guild = None

# SMs
ryan_sm = bot.get_user(1008913569871564811)
a380_sm = bot.get_user(828522170342703136)
speedbird_sm = bot.get_user(993882436775727246)

# Roles
emergency_ping = None
server_manager = None
server_mod = None

@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    if message.author == bot.user:
        return
    if "apply" in user_message.lower():
        text_channel = bot.get_channel(1091962173791666286)
        await message.channel.send(f"Hello {message.author.mention}, please go to {text_channel.mention} to apply!")
    await bot.process_commands(message)

class ATCPanelView(discord.ui.View):
    def __init__(self, embed, airport, dm):
        super().__init__()
        self.embed = embed
        self.airport = airport
        self.dm = dm

    @discord.ui.button(label="Toggle ATC", style=discord.ButtonStyle.red)
    async def toggle_atc(self, interaction: discord.Interaction, button: discord.Button):
        global atc_status
        for key, value in atc_status.items():
            if value[0] == interaction.user.id:
                atc_status[key][0] = False
                self.children[0].disabled = True
                self.children[1].disabled = True
            elif value[0] == False:
                atc_status[key] = [interaction.user.id, ""]
                self.children[1].disabled = False
        if value[0] == interaction.user.id: await self.dm.send("Stopped ATC.")
        await interaction.response.edit_message(view=self, embed=self.embed)
    
    @discord.ui.button(label="Change or Modify ATIS", style=discord.ButtonStyle.green, disabled=True)
    async def request_atis(self, interaction: discord.Interaction, button: discord.Button):
        global atc_status
        atis_information = bot.get_channel(1091941405456334858)
        await interaction.response.send_message("Type in your ATIS below.")
        atis = await bot.wait_for('message')
        for key, value in atc_status.items():
            if value[0] == interaction.user.id:
                atc_status[key][1] = str(atis.content)
        await interaction.followup.send("Your ATIS is:\n" + str(atis.content))
        embed = discord.Embed(title=f"ATIS from Airport {self.airport}", description=str(atis.content))
        await atis_information.send(embed=embed)

@bot.tree.command(name = "atc", description = "Request ATC.")
async def atc(interaction: discord.Interaction, airport: str):
    global atc_status   
    apt = airport.lower()
    if apt in AIRPORT_NAMES:
        status = atc_status[apt]
        if status[0] == False:
            await interaction.response.send_message(f"Check Your DMs for Further Instructions. You are now ATC of the Airport {airport}.")
            dm = await interaction.user.create_dm()
            embed = discord.Embed(title="Welcome to ATC!!", description=f"Currently, you are the ATC of {airport}!\nPress the red button that says `TOGGLE ATC` to get started.\nAfter that, press `CHANGE ATIS` to change your ATIS, then press `SEND ATIS` to send the ATIS out to Atis-Information.\nHappy Controlling!")
            view = ATCPanelView(embed=embed, airport=airport, dm=dm)
            await dm.send(embed=embed, view=view)
        else:
            await interaction.response.send_message(f"There is already an active ATC for the Airport {airport}.")
    else:
        await interaction.response.send_message(f"Your Airport Requested, {airport}, Does Not Exist.")

@bot.tree.command(name = "flightplan", description = "File a Flightplan.")
async def flightplan_file(interaction: discord.Interaction):
    dms = await interaction.user.create_dm()
    embed = discord.Embed(title="Welcome to ATC 48 Flightplan Creator!", description="You will be prompted with a few questions to create a flightplan.\nMake sure that you are entering correct airport names.\n**Trolling with the FP Creator WILL result in a warn, and in severe cases, a ban.**")
    await dms.send(embed=embed) 
    await interaction.response.send_message("Check DMs for Creating a Flightplan.")
    questions = ["What is your Callsign?", "What is your Aircraft?", "VFR or IFR?", "What is your Departure Airport?", "What is your Arrival Airport?", "What is your Desired Route?", "What is your crusing altitude?", "What is your SQUAWK?"]
    answers = []
    for question in questions:
        await dms.send(question)
        answer = await bot.wait_for('message', check=lambda message: message.author == interaction.user)
        answers.append(str(answer.content))
    submit_channel = bot.get_channel(1091941368819089418)
    flight = f"""User: {interaction.user.mention}
Callsign: {answers[0]}
Aircraft: {answers[1]}
VFR/IFR: {answers[2]}
Departure: {answers[3]}
Arrival: {answers[4]}
Route: {answers[5]}
Altitude: {answers[6]}
Squawk: {answers[7]}
    """
    submit_flightplan = discord.Embed(title=f"**Flightplan for {answers[0]}**", description=flight)
    await submit_channel.send(embed=submit_flightplan)

    submit_message = discord.Embed(title="Thank you for using the ATC 48 Flightplan Creator!", description="Your flight plan has been sent to ATCs and in the channel #flight-plans.\nThank you for playing ATC 48!\nHave a safe flight! ✈")
    await dms.send(embed=submit_message)

@bot.tree.command(name = "em", description = "Emergency Ping. USE ONLY IN SEVERE EMERGENCIES.")
async def em(interaction: discord.Interaction):
    managers_channel = bot.get_channel(1091939198853980293)
    await managers_channel.send(f"EMERGENCY PING! REPORT OVER TO THE SERVER IMMEDIATLY.\n{emergency_ping.mention}")
    await interaction.response.send_message("Sent a Emergency Ping to the Managers.")

@bot.event
async def on_ready():
    global guild, emergency_ping, server_manager, server_mod
    synced = await bot.tree.sync()

    activity = discord.Game(name="ATC 48", type=3)
    await bot.change_presence(activity=activity)

    print(f"Synced {len(synced)} command(s)")

    guild = bot.get_guild(1091939198853980290)

    emergency_ping = guild.get_role(1105660282665173073)
    server_manager = guild.get_role(1091942770643583117)
    server_mod = guild.get_role(1091943003578449920)

bot.run(TOKEN)