import discord
from discord import app_commands
from discord.ext import commands

from confidential import LOGS_CHANNEL_ID
from db.dbfunc import (get_banned_list_as_str, get_election_channel_id,
                       get_preview_channel_id)
from persistent_views import ElectionView, PreviewView
from utils import create_embed, send, str_to_list
from views import url_view


class Nomination(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="nominate")
    @app_commands.describe(
        attachment="Attachment of the emoji as a picture or gif",
        name="Name you wish to call the emoji",
    )
    async def nominate(
        self,
        interaction: discord.Interaction,
        attachment: discord.Attachment,
        name: str,
    ):
        """Nominate an image or gif that should be added to this server!"""
        logs_channel = self.client.get_channel(LOGS_CHANNEL_ID)
        await logs_channel.send("nominate command called")
        accepted_content_types = ["image/png", "image/jpeg", "image/gif"]

        if attachment.content_type not in accepted_content_types:
            await send(
                interaction,
                create_embed(
                    "Error",
                    "Your attachment must be either a PNG, JPEG, or GIF file type, as these are the only types that Discord allows for emoji. Please try again with a different file type.",
                    discord.Color.red(),
                ),
                view=url_view,
                ephemeral=True,
            )
            return
        elif attachment.content_type == "image/gif" and attachment.size > 2097152:
            await send(
                interaction,
                create_embed(
                    "Error",
                    "Your GIF attachment exceeds the 2 MB limit for emoji uploads on discord :( Please shrink the size of your GIF and try again.",
                    discord.Color.red(),
                ),
                view=url_view,
                ephemeral=True,
            )
            return
        elif attachment.size > 262144:
            await send(
                interaction,
                create_embed(
                    "Error",
                    "Your PNG or JPEG attachment exceeds the 256 KB limit for picture emoji uploads on discord :( Please shrink your image and try again.",
                    discord.Color.red(),
                ),
                view=url_view,
                ephemeral=True,
            )
            return

        await nomination_logic(self.client, interaction, attachment.url, name)


async def nomination_logic(
    client: commands.Bot, interaction: discord.Interaction, image_url: str, name: str
):
    """Handles the concurrent logic between nomination commands."""
    ban_list = str_to_list(get_banned_list_as_str(interaction.guild_id))
    if interaction.user.id in ban_list:
        await send(
            interaction,
            create_embed(
                "Error",
                "You are banned from nominating emojis in this server. Reach out to a moderator for more information.",
                discord.Color.red(),
            ),
            view=url_view,
            ephemeral=True,
        )
        return
    preview_channel_id = get_preview_channel_id(interaction.guild_id)
    if preview_channel_id:
        preview_channel = client.get_channel(preview_channel_id)
        embed = nomination_embed(interaction, name)
        embed.set_image(url=image_url)
        await preview_channel.send(embed=embed, view=PreviewView())
        await send(
            interaction,
            embed=nomination_success_embed(),
            view=url_view,
            ephemeral=True,
        )
    else:
        election_channel_id = get_election_channel_id(interaction.guild_id)
        if election_channel_id:
            election_channel = client.get_channel(election_channel_id)
            embed = nomination_embed(interaction, name)
            embed.set_image(url=image_url)
            election_message = await election_channel.send(
                embed=embed, view=ElectionView()
            )
            if type(election_message) == discord.Message:
                await election_message.add_reaction("👍")
                await election_message.add_reaction("👎")
            await send(
                interaction,
                embed=nomination_success_embed(preview_channel=False),
                view=url_view,
                ephemeral=True,
            )
        else:
            title = "Nomination Error"
            description = "Either the election or preview channel needs to be set before nominating emojis. \
                A user with `Manage Server` permissions must use either the `set-election-channel` or `set-preview-channel` commands."
            colour = discord.Colour.red()
            await send(
                interaction,
                create_embed(title, description, colour),
                url_view,
                ephemeral=True,
            )


def nomination_embed(interaction: discord.Interaction, name: str) -> discord.Embed:
    """Creates the base nomination embed"""
    title = f"Nomination from {interaction.user.name}"
    description = f"Emoji Name: {name}"
    colour = discord.Colour.dark_orange()
    return create_embed(title, description, colour)


def nomination_success_embed(preview_channel: bool = True) -> discord.Embed:
    channel = "preview" if preview_channel else "election"
    title = "Nomination Success!"
    description = f"Your emoji nomination has been sent to the emoji {channel} channel. Good luck!"
    colour = discord.Colour.green()
    return create_embed(title, description, colour)


async def setup(client):
    await client.add_cog(Nomination(client))
