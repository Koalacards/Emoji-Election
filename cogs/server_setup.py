import discord
from discord import app_commands
from discord.ext import commands

from db.dbfunc import set_election_channel_id, set_preview_channel_id
from utils import send, create_embed
from views import url_view

class ServerSetup(commands.Cog):
    def __init__(self, client) -> None:
        self.client=client

    @app_commands.command(name="set-election-channel")
    @app_commands.describe(election_channel="Which channel in your server you want to have emoji elections in?")
    @app_commands.default_permissions(manage_guild = True)
    async def set_election_channel(self, interaction:discord.Interaction, election_channel:discord.TextChannel):
        """Set the channel in your server you will have emoji elections in. This must be set before users can nominate emojis."""
        election_channel_id = election_channel.id
        set_election_channel_id(interaction.guild_id, election_channel_id)
        embed = create_embed("Election Channel Set Successfully", "", discord.Color.green())
        await send(interaction, embed, url_view)

    
    @app_commands.command(name="set-preview-channel")
    @app_commands.describe(preview_channel="Which channel in your server you want to preview emoji nominations in?")
    @app_commands.default_permissions(manage_guild = True)
    async def set_preview_channel(self, interaction:discord.Interaction, preview_channel:discord.TextChannel):
        """Set the channel in your server you can preview emojis in and give a yes/no on whether they are appropriate for voting.
        If this channel is not set, all nominated emojis will automatically show up in the emoji election channel.
        """
        preview_channel_id = preview_channel.id
        set_preview_channel_id(interaction.guild_id, preview_channel_id)
        embed = create_embed("Preview Channel Set Successfully", "", discord.Color.green())
        await send(interaction, embed, url_view)

async def setup(client):
    await client.add_cog(ServerSetup(client))