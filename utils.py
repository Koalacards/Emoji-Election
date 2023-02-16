import discord

def create_embed(title, description, colour):
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed

async def send(
    interaction: discord.Interaction, embed: discord.Embed, view: discord.ui.View
):
    await interaction.response.send_message(embed=embed, view=view)