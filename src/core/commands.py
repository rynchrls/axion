import discord
from discord import app_commands


class MyCommands(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Sync commands globally (can take up to 1 hour to appear everywhere)
        await self.tree.sync()
        print("✅ Global commands synced!")
