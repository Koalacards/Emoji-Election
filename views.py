# These are just views that don't have to be loaded persistently- those who do live in persistent_views.py
import discord
from discord.ui import Button, View

## URL buttons for setup commands, help command, and nominate command

invite_button = Button(
    label="Invite",
    style=discord.ButtonStyle.url,
    url="https://discord.com/api/oauth2/authorize?client_id=1075591979863392298&permissions=3221507072&scope=bot%20applications.commands",
)

support_button = Button(
    label="Discord Server",
    style=discord.ButtonStyle.url,
    url="https://discord.gg/5Jn32Upk4M",
)

github_button = Button(
    label="Github",
    style=discord.ButtonStyle.url,
    url="https://github.com/Koalacards/Emoji-Election",
)

url_buttons = [invite_button, support_button, github_button]
url_view = View()
for button in url_buttons:
    url_view.add_item(button)
