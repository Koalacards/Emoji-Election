## Persistent Views, or views that have to be loaded even if the bot goes offline
import discord
import requests
from discord.ui import Select, View

from db.dbfunc import get_election_channel_id
from utils import create_embed, send

## View for messages in the preview Channel


class PreviewDropdown(Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="Approve Nomination",
                description="This will send the nomination to the election channel or add the emoji if no election channel.",
                emoji="✅",
            ),
            discord.SelectOption(
                label="Reject Nomination",
                description="This will not allow the nomination to go through to the election phase or become an emoji",
                emoji="🚫",
            ),
        ]

        super().__init__(
            custom_id="preview_dropdown",
            placeholder="Preview Options (Mods only)",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if (
            not user.guild_permissions.manage_guild
            and not user.guild_permissions.administrator
        ):
            await send(
                interaction,
                create_embed(
                    "Error",
                    "You must have `Manage Server` or `Administrator` permissions to select an action.",
                    discord.Color.red(),
                ),
                ephemeral=True,
            )
            return

        message = interaction.message
        message_embed = message.embeds[0]
        user_mention = message_embed.title[16:]
        emoji_name = message_embed.description[12:]
        approved_str = "Approved"
        colour = discord.Color.green()

        option_chosen = self.values[0]
        if option_chosen == "Approve Nomination":
            election_channel_id = get_election_channel_id(interaction.guild_id)
            if election_channel_id is None:
                img_bytes = requests.get(message_embed.image.url).content
                await interaction.guild.create_custom_emoji(
                    name=emoji_name, image=img_bytes
                )
            else:
                election_channel = interaction.client.get_channel(election_channel_id)
                election_message = await election_channel.send(
                    embed=message_embed, view=ElectionView()
                )
                if type(election_message) == discord.Message:
                    await election_message.add_reaction("👍")
                    await election_message.add_reaction("👎")
        elif option_chosen == "Reject Nomination":
            approved_str = "Rejected"
            colour = discord.Color.red()

        await message.edit(
            embed=create_embed(
                f"Emoji From {user_mention}: {approved_str} in Preview Channel",
                f"Emoji Name: {emoji_name}",
                colour,
            ),
            view=None,
        )
        return


class PreviewView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PreviewDropdown())


# View for messages in the election channel


class ElectionDropdown(Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="Approve Nomination",
                description="This will add the emoji to the server.",
                emoji="✅",
            ),
            discord.SelectOption(
                label="Reject Nomination",
                description="This will reject the emoji from being added to the server.",
                emoji="🚫",
            ),
        ]

        super().__init__(
            custom_id="election_dropdown",
            placeholder="Election Options (Mods only)",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if (
            not user.guild_permissions.manage_guild
            and not user.guild_permissions.administrator
        ):
            await send(
                interaction,
                create_embed(
                    "Error",
                    "You must have `Manage Server` or `Administrator` permissions to select an action.",
                    discord.Color.red(),
                ),
                ephemeral=True,
            )
            return

        message = interaction.message
        message_embed = message.embeds[0]
        user_mention = message_embed.title[16:]
        emoji_name = message_embed.description[12:]
        approved_str = "Approved"
        colour = discord.Color.green()

        option_chosen = self.values[0]
        if option_chosen == "Approve Nomination":
            img_bytes = requests.get(message_embed.image.url).content
            await interaction.guild.create_custom_emoji(
                name=emoji_name, image=img_bytes
            )
        elif option_chosen == "Reject Nomination":
            approved_str = "Rejected"
            colour = discord.Color.red()

        await message.edit(
            embed=create_embed(
                f"Emoji From {user_mention}: {approved_str}",
                f"Emoji Name: {emoji_name}",
                colour,
            ).set_image(url=message_embed.image.url),
            view=None,
        )
        return


class ElectionView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ElectionDropdown())
