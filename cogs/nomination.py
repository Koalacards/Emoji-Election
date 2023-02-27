import discord
from discord import app_commands
from discord.ext import commands

from db.dbfunc import get_election_channel_id, get_preview_channel_id
from utils import create_embed, send
from views import url_view


class Nomination(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client=client

    
    @app_commands.command(name="nominate")
    @app_commands.describe(emoji="Attachment of the emoji as a picture or gif", name="Name you wish to call the emoji")
    async def nominate(self, interaction: discord.Interaction, emoji: discord.Attachment, name: str):
        """Nominate an emoji that should be added to this server! Will be sent to a preview channel for moderation or an election channel for voting."""
        preview_channel_id = get_preview_channel_id(interaction.guild_id)
        if preview_channel_id:
            preview_channel = self.client.get_channel(preview_channel_id)
            embed=nomination_embed(interaction, name)
            embed.set_image(url=emoji.url)
            await preview_channel.send(embed=embed)
            await send(interaction, embed=nomination_success_embed(), view=url_view, ephemeral=True)
        else:
            election_channel_id = get_election_channel_id(interaction.guild_id)
            if election_channel_id:
                election_channel = self.client.get_channel(election_channel_id)
                embed=nomination_embed(interaction, name)
                embed.set_image(url=emoji.url)
                await election_channel.send(embed=embed)
                await send(interaction, embed=nomination_success_embed(preview_channel=False), view=url_view, ephemeral=True)
            else:
                title="Nomination Error"
                description="Either the election or preview channel needs to be set before nominating emojis. \
                 A user with `Manage Server` permissions must use either the `set-election-channel` or `set-preview-channel` commands."
                colour = discord.Colour.red()
                await send(interaction, create_embed(title, description, colour), url_view, ephemeral=True)
        


def nomination_embed(interaction:discord.Interaction, name: str) -> discord.Embed:
    """Creates the base nomination embed"""
    title = f"Nomination from {interaction.user.name}"
    description=f"Emoji Name: {name}"
    colour= discord.Colour.dark_orange()
    return create_embed(title, description, colour)


def nomination_success_embed(preview_channel:bool = True) -> discord.Embed:
    channel = "preview" if preview_channel else "election"
    title = "Nomination Success!"
    description = f"Your emoji nomination has been sent to the emoji {channel} channel. Good luck!"
    colour = discord.Colour.green()
    return create_embed(title, description, colour)


async def setup(client):
    await client.add_cog(Nomination(client))