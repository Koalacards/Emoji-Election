import discord
from discord import app_commands
from discord.ext import commands

from db.dbfunc import (get_banned_list_as_str, set_banned_list_str,
                       set_election_channel_id, set_preview_channel_id)
from utils import create_embed, send, str_to_list
from views import url_view
from confidential import LOGS_CHANNEL_ID


class ServerSetup(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.logs_channel = self.client.get_channel(LOGS_CHANNEL_ID)

    @app_commands.command(name="set-election-channel")
    @app_commands.describe(
        election_channel="Which channel in your server you want to have emoji elections in?"
    )
    @app_commands.default_permissions(manage_guild=True)
    async def set_election_channel(
        self, interaction: discord.Interaction, election_channel: discord.TextChannel
    ):
        """Set the channel in your server you will have emoji elections in. If this channel is not set, then the preview channel
        will be used and any yes's in the preview channel will be automatically added as emojis."""
        await self.logs_channel.send("set-election-channel command called")
        election_channel_id = election_channel.id
        set_election_channel_id(interaction.guild_id, election_channel_id)
        embed = create_embed(
            "Election Channel Set Successfully", "", discord.Color.green()
        )
        await send(interaction, embed, url_view)

    @app_commands.command(name="set-preview-channel")
    @app_commands.describe(
        preview_channel="Which channel in your server you want to preview emoji nominations in?"
    )
    @app_commands.default_permissions(manage_guild=True)
    async def set_preview_channel(
        self, interaction: discord.Interaction, preview_channel: discord.TextChannel
    ):
        """Set the channel in your server you can preview emojis in and give a yes/no on whether they are appropriate for voting.
        If this channel is not set, all nominated emojis will automatically show up in the emoji election channel.
        """
        await self.logs_channel.send("set-preview-channel command called")
        preview_channel_id = preview_channel.id
        set_preview_channel_id(interaction.guild_id, preview_channel_id)
        embed = create_embed(
            "Preview Channel Set Successfully", "", discord.Color.green()
        )
        await send(interaction, embed, url_view)

    @app_commands.command(name="ban")
    @app_commands.describe(user="User to ban.")
    @app_commands.default_permissions(manage_guild=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User):
        """Ban a member from nominating emojis in your server."""
        await self.logs_channel.send("ban command called")
        ban_list = str_to_list(get_banned_list_as_str(interaction.guild_id))
        if user.id in ban_list:
            await send(
                interaction,
                create_embed(
                    "Error", f"User {user.name} is already banned.", discord.Color.red()
                ),
                view=url_view,
                ephemeral=True,
            )
        else:
            ban_list.append(user.id)
            set_banned_list_str(interaction.guild_id, str(ban_list))
            await send(
                interaction,
                create_embed(
                    "Success",
                    f"User {user.name} banned successfully!",
                    discord.Color.green(),
                ),
                view=url_view,
                ephemeral=True,
            )

    @app_commands.command(name="unban")
    @app_commands.describe(user="User to unban.")
    @app_commands.default_permissions(manage_guild=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User):
        """Unban a member from nominating emojis in your server."""
        await self.logs_channel.send("unban command called")
        ban_list = str_to_list(get_banned_list_as_str(interaction.guild_id))
        if user.id not in ban_list:
            await send(
                interaction,
                create_embed(
                    "Error",
                    f"User {user.name} is already unbanned.",
                    discord.Color.red(),
                ),
                view=url_view,
                ephemeral=True,
            )
        else:
            ban_list.remove(user.id)
            set_banned_list_str(interaction.guild_id, str(ban_list))
            await send(
                interaction,
                create_embed(
                    "Success",
                    f"User {user.name} unbanned successfully!",
                    discord.Color.green(),
                ),
                view=url_view,
                ephemeral=True,
            )


async def setup(client):
    await client.add_cog(ServerSetup(client))
