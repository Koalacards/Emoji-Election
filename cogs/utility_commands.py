import discord
from discord import app_commands
from discord.ext import commands

from utils import send, create_embed
from views import url_view
from confidential import SUGGESTION_CHANNEL_ID, LOGS_CHANNEL_ID

class UtilityCommands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction) -> None:
        """Displays the commands to use Emoji Election!"""
        logs_channel = self.client.get_channel(LOGS_CHANNEL_ID)
        await logs_channel.send("help command called")
        title = "Emoji Election Help Page"
        description = (
            "Thanks for adding Emoji Election to your server! This very simple bot gives you the ability to nominate and vote emojis that should be added to a server!\n\n"
            "**Commands For All Users**\n\n"
            "**nominate**: Nominate and name an attachment (PNG, JPEG, or GIF) that you think should be an emoji in the server! Once your nomination goes through, it will either be sent to the preview or election channel in your server for viewing.\n\n"
            "**suggest**: Make a suggestion or report a bug directly to the Emoji Election devs!\n\n"
            "**Setup Commands (For Mods Only)**\n\n"
            "**set-preview-channel**: Set a channel where you can manually approve and decline nominations. This is a way to check that nominations are appropriate before moving to the election channel. If you do **not** have an election channel set, approved nominations in the preview channel will be added as emojis to the server.\n\n"
            "**set-election-channel**: Set a channel where users can vote up/down on emojis and you can approve/decline emojis to be added to the server. If you do not set up a preview channel, nominated emojis will automatically go here instead of the preview channel first.\n\n"
            "**ban**: Ban a user from nominating emojis in this server.\n\n"
            "**unban**: Unban a user from nominating emojis in this server.\n\n"
            "Happy electing!"
        )
        color = discord.Color.dark_orange()
        await send(
            interaction,
            create_embed(title, description, color),
            view=url_view
        )
    

    @app_commands.command(name="suggest")
    @app_commands.describe(suggestion="Something to suggest for the Emoji Election devs!")
    async def suggest(self, interaction: discord.Interaction, suggestion: str) -> None:
        """Suggest an improvement or report a bug regarding the Emoji Election bot!"""
        logs_channel = self.client.get_channel(LOGS_CHANNEL_ID)
        await logs_channel.send("suggest command called")
        suggestion_channel = self.client.get_channel(SUGGESTION_CHANNEL_ID)
        await suggestion_channel.send(
            embed=create_embed(
                f"New Suggestion from {interaction.user.name}",
                suggestion,
                discord.Color.dark_orange()
            )
        )

        await send(
            interaction,
            create_embed(
                "Success!",
                "Your suggestion or report has been sent to the devs, thank you for supporting Emoji Election!",
                discord.Color.green()
            ),
            view=url_view,
            ephemeral=True
        )




async def setup(client):
    await client.add_cog(UtilityCommands(client))