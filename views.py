from discord import ButtonStyle
from discord.ui import Button, View

## URL buttons for setup commands, help command, and nominate command

invite_button = Button(
    label="Invite",
    style=ButtonStyle.url,
    url = "https://discord.com/api/oauth2/authorize?client_id=1075591979863392298&permissions=3221507072&scope=bot%20applications.commands"
)

support_button = Button(
    label="Support",
    style=ButtonStyle.url,
    url="https://discord.gg/5Jn32Upk4M"
)

url_buttons= [invite_button, support_button]
url_view = View()
for button in url_buttons:
    url_view.add_item(button)
