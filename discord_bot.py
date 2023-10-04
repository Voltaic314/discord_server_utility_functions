import asyncio
import os
import discord
from discord import app_commands
import config


class Bot(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Enable the GUILD_MEMBERS intent
        intents.messages = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.synced = False  # we use this so the bot doesn't sync commands more than once
        # define our variables
        self.server_id = config.discord_bot_credentials["Server_ID"]
        self.SELF_CARE_CHANNEL_ID = config.discord_bot_credentials["Self_Care_Channel_ID"]
        self.user_id = config.discord_bot_credentials["Client_ID"]

        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        if not self.synced:  # check if slash commands have been synced
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")


if __name__ == "__main__":
    client = Bot()
    tree = app_commands.CommandTree(client)
    TOKEN = config.discord_bot_credentials["API_Key"]
    client.run(TOKEN)
