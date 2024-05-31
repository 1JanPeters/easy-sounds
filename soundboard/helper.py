import pickle
import os
import discord

def load_sounds(SOUNDS_FOLDER):
    sounds = {}
    for filename in os.listdir(SOUNDS_FOLDER):
        if filename.endswith(('.mp3', '.wav')):
            sound_name = os.path.splitext(filename)[0]
            sounds[sound_name] = filename
    return sounds

def save_user_sound_mapping(PERSISTENCE_FILE, user_sound_mapping):
    with open(PERSISTENCE_FILE, 'wb') as f:
        pickle.dump(user_sound_mapping, f)

def load_user_sound_mapping(PERSISTENCE_FILE):
    if os.path.exists(PERSISTENCE_FILE):
        with open(PERSISTENCE_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def convert_to_seconds(time_str):
    parts = time_str.split(':')
    seconds = float(parts[-1])
    minutes = float(parts[-2]) if len(parts) > 1 else 0
    hours = float(parts[-3]) if len(parts) > 2 else 0
    return seconds + minutes * 60 + hours * 3600

def parse_arguments(args, keys):
    args_list = args.split()
    args_dict = {key: None for key in keys}
    current_arg = None
    collected_name = []
    for arg in args_list:
        if arg in args_dict:
            if collected_name and current_arg == '-n':
                args_dict[current_arg] = ' '.join(collected_name)
                collected_name = []
            current_arg = arg
        elif current_arg:
            if current_arg == '-n':
                collected_name.append(arg)
            else:
                args_dict[current_arg] = arg
                current_arg = None

    if collected_name and current_arg == '-n':
        args_dict[current_arg] = ' '.join(collected_name)

    return args_dict

async def connect_to_voice_channel(voice_channel):
    return await voice_channel.connect(self_deaf=True)

async def play_sound(sound_file, voice_channel, SOUNDS_FOLDER, bot):
    try:
        voice_client = None
        for client in bot.voice_clients:
            if client.channel == voice_channel:
                voice_client = client
                break

        if voice_client is None:
            voice_client = await connect_to_voice_channel(voice_channel)

        if voice_client.is_playing():
            voice_client.stop()

        source = discord.FFmpegPCMAudio(os.path.join(SOUNDS_FOLDER, sound_file))
        voice_client.play(source)
    except Exception as e:
        print(f"Error playing sound via button: {e}")
