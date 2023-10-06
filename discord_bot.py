import asyncio
import os
import discord
from discord import app_commands
import config
import find_duplicate_emojis


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


@tree.command(name="find_duplicate_emotes", description="Responds with a list of potential duplicate emotes in the server's emote list")
async def Duplicate_Emote_command(Interaction: discord.Interaction):
    await Interaction.response.defer()

    emote_list = get_static_emotes()

    potential_duplicates = find_duplicates_through_hashes(emote_list)

    if not potential_duplicates:
        formatted_string_to_send_to_channel = 'There were no duplicates found!'
        Interaction.channel.send(formatted_string_to_send_to_channel)

    else:

        formatted_string_to_send_to_channel = ''
        formatted_string_to_send_to_channel += f'Found: {len(potential_duplicates)} emotes with potential duplicates.'
        formatted_string_to_send_to_channel += 'Here are a list of emote names and their potential duplicates to check:'

        for emote, duplicate_list in potential_duplicates.items():

            duplicate_list_string = ', '.join(duplicate_list)

            formatted_string_to_send_to_channel += f'Emote: {emote.name}, Potential Duplicate Emotes: {duplicate_list_string}'

        Interaction.channel.send(formatted_string_to_send_to_channel)



if __name__ == "__main__":
    client = Bot()
    tree = app_commands.CommandTree(client)
    TOKEN = config.discord_bot_credentials["API_Key"]
    client.run(TOKEN)
