import discord
from typing import Optional

def create_embed(title: str, description: str, colour: discord.Color) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed

async def send(
    interaction: discord.Interaction, embed: discord.Embed, view: Optional[discord.ui.View] = None
):
    if view:
        await interaction.response.send_message(embed=embed, view=view)
    else:
        await interaction.response.send_message(embed=embed)