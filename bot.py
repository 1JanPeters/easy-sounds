import os
import json
import discord
from discord.ext import commands
import soundboard.commands as sb_commands, soundboard.events as events, soundboard.helper as helper

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')
# Load configuration from file
with open(config_path, mode='r', encoding='UTF-8') as config_file:
    config = json.load(config_file)

TOKEN = config['TOKEN']
GUILD_ID = int(config['GUILD_ID'])
SOUNDBOARD_CHANNEL_ID = int(config['SOUNDBOARD_CHANNEL_ID'])

# Ensure the necessary intents are enabled
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents, case_insensitive=False)
tree = bot.tree

SOUNDS_FOLDER = config['SOUNDS_FOLDER']
PERSISTENCE_FILE = 'user_sound_mapping.pkl'

# Load or initialize user sound mapping
user_sound_mapping = helper.load_user_sound_mapping(PERSISTENCE_FILE)

# Register commands and events
sb_commands.register_commands(tree, bot, SOUNDS_FOLDER, GUILD_ID, PERSISTENCE_FILE, 
                              SOUNDBOARD_CHANNEL_ID, user_sound_mapping)
events.register_events(bot, SOUNDS_FOLDER, GUILD_ID, SOUNDBOARD_CHANNEL_ID, user_sound_mapping)

# Start the bot
bot.run(TOKEN)
