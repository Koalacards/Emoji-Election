import discord
from discord.ext import commands, tasks

from confidential import RUN_ID
from persistent_views import ElectionView, PreviewView


class EmojiElectionClient(commands.Bot):
    def __init__(self, *, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self) -> None:
        await client.load_extension("cogs.server_setup")
        await client.load_extension("cogs.nomination")
        await client.load_extension("cogs.utility_commands")
        self.add_view(PreviewView())
        self.add_view(ElectionView())
        await self.tree.sync()

    async def on_ready(self):
        self.update_presence.start()
        print("ready")

    @tasks.loop(minutes=30)
    async def update_presence(self):
        guild_count = str(len(client.guilds))
        await client.change_presence(
            activity=discord.Game(
                name=f"/help in {guild_count} servers! Emoji Responsibly :-)"
            )
        )


intents = discord.Intents.default()

intents.messages = True
intents.message_content = True
client = EmojiElectionClient(command_prefix="~~~", intents=intents)

client.run(RUN_ID)
