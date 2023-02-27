import discord
from discord.ui import Button, View, Select
from db.dbfunc import get_election_channel_id

## URL buttons for setup commands, help command, and nominate command

invite_button = Button(
    label="Invite",
    style=discord.ButtonStyle.url,
    url = "https://discord.com/api/oauth2/authorize?client_id=1075591979863392298&permissions=3221507072&scope=bot%20applications.commands"
)

support_button = Button(
    label="Support",
    style=discord.ButtonStyle.url,
    url="https://discord.gg/5Jn32Upk4M"
)

url_buttons= [invite_button, support_button]
url_view = View()
for button in url_buttons:
    url_view.add_item(button)


## View for messages in the preview Channel

class PreviewDropdown(Select):
    def __init__(self):

        options = [
            discord.SelectOption(label="Approve Nomination", description="If approved, this nomination will either be sent to the election channel or the emoji will be added if no election channel exists.", emoji="✅"),
            discord.SelectOption(label="Reject Nomination", description="This will not allow the nomination to go through to the election phase or become an emoji", emoji="🚫")
        ]

        super().__init__(placeholder='Preview Options (Mods only)', min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        message = interaction.message
        message_embed = interaction.message.embeds[0]
        option_chosen = self.values[0]
        if option_chosen == "Approve Nomination":
            election_channel_id = get_election_channel_id(interaction.guild_id)
            if election_channel_id is None:
                await interaction.guild.create_custom_emoji(name="temp_name", image=message_embed.image)
            else:
                election_channel = interaction.client.get_channel(election_channel_id)
                await election_channel.send(embed=message_embed)
            #Edit existing message

        
