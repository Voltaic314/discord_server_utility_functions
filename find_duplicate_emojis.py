import os
import discord
from discord import app_commands
from discord_bot import Bot
from PIL import Image
import imagehash
import requests
from emote import Emote


client = Bot()
tree = client.tree



def get_static_emotes() -> list[object]:
    
    # first get the list of emotes from the server. (This will actually be a tuple).
    guild = client.get_guild(client.server_id)
    tuple_of_emote_objects = guild.emojis

    # iterate through the emotes and only create a list of emote objects from static image emotes
    list_of_emotes = []
    for emote in tuple_of_emote_objects:
        if not emote.animated:
            list_of_emotes.append(Emote(url=emote.url))

    return list_of_emotes


def find_duplicates_through_hashes(list_of_emotes: list[object]) -> dict[object: object]:
    '''
    This function will go through the list of emote objects and compare their hashes
    to find duplicates. For more information on this go here: https://pypi.org/project/ImageHash/
    It will then return a dictionary objects with the emote objects as keys and a list
    of all potential duplicates as the values for that emote.

    Parameters: list of emote objects, must contain their hash attribute.

    Returns: Dictionary object - keys are the original emote, list of other similar emote as values
    '''
    dictionary_of_ids_and_duplicate_ids = {}

    ideal_hamming_distance_for_hashes = 8

    # Check each emote's hash
    for emote in list_of_emotes:
        dictionary_of_ids_and_duplicate_ids[emote] = []
        for second_emote in list_of_emotes:
            
            # FIXME: This is a big O(n^2) algorithm, this should be further improved for efficiency
            # Luckily you can only have up to 50 static emotes so this is just 2500 comparisons at max.
            if emote != second_emote:
                if  emote.hash_string - second_emote.hash_string >= ideal_hamming_distance_for_hashes:
                    dictionary_of_ids_and_duplicate_ids[emote].append(second_emote)

    return dictionary_of_ids_and_duplicate_ids



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
