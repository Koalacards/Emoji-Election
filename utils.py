import json
from typing import Optional

import discord


def create_embed(title: str, description: str, colour: discord.Color) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed


async def send(
    interaction: discord.Interaction,
    embed: discord.Embed,
    view: Optional[discord.ui.View] = None,
    ephemeral: bool = False,
):
    if view:
        await interaction.response.send_message(
            embed=embed, view=view, ephemeral=ephemeral
        )
    else:
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


def str_to_list(list_as_str: str) -> list:
    json_compatible = list_as_str.replace("'", '"')
    return json.loads(json_compatible)
