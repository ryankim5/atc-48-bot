import discord

class ATCPanelView(discord.ui.View):
    @discord.ui.button(label="Change or Modify ATIS", style=discord.ButtonStyle.green)
    async def request_atis(self, interaction: discord.Interaction, button: discord.Button):
        global atc_status   
        custom_id = interaction.data["custom_id"]
        cid = custom_id.split("|")  
        await interaction.response.send_message("Type in your ATIS below.")
        atis = await bot.wait_for('message')
        atc_status[cid[0]][1] = str(atis.content)
        await interaction.followup.send("Your ATIS is:\n" + str(atis.content))

    @discord.ui.button(label="Stop ATC", style=discord.ButtonStyle.red)
    async def atc_stop(self, interaction: discord.Interaction, button: discord.Button):
        global atc_status
        custom_id = interaction.data["custom_id"]
        cid = custom_id.split("|")
        atc_status[cid[0]] = [False, False]
        await interaction.response.send_message("Stopped ATC.")
        for b in self.view.children:
            b.disabled = True
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label="Send ATIS")
    async def send_atis(self, interaction: discord.Interaction, button: discord.Button):
        submit_channel = bot.get_channel(1091941405456334858)
        for key, value in atc_status: