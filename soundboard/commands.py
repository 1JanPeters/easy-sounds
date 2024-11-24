import discord
from discord import app_commands
import os
import re
from moviepy.editor import AudioFileClip
import soundboard.helper as helper
import soundboard.sound_management as sound_management
import soundboard.soundboard_view as soundboard_view
from yt_dlp import YoutubeDL



def register_commands(tree, bot, SOUNDS_FOLDER, GUILD_ID, PERSISTENCE_FILE, SOUNDBOARD_CHANNEL_ID, user_sound_mapping):
    @tree.command(name="setjoinsound", description="Set a sound to play when you join a voice channel.")
    @app_commands.describe(sound_name="The name of the sound to play.")
    async def setjoinsound(interaction: discord.Interaction, sound_name: str):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You are not in a voice channel.")
            return

        sound_file = f"{sound_name}.mp3"
        if not os.path.exists(os.path.join(SOUNDS_FOLDER, sound_file)):
            await interaction.response.send_message(f"Sound '{sound_name}' not found.")
            return

        user_sound_mapping[interaction.user.id] = sound_file
        helper.save_user_sound_mapping(PERSISTENCE_FILE, user_sound_mapping)
        await interaction.response.send_message(f"Sound '{sound_name}' set for {interaction.user.display_name}.")

    @tree.command(name="deletesound", description="Delete a sound file from the soundboard.")
    async def deletesound(interaction: discord.Interaction, sound_name: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await sound_management.delete_sound(interaction, sound_name, SOUNDS_FOLDER)
        await create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID, SOUNDS_FOLDER)

    @tree.command(name="rename", description="Rename a sound file. \\rename \"old\" \"new\"")
    async def rename(interaction: discord.Interaction, *, args: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        match = re.match(r'^"(.+?)"\s+"(.+?)"$', args)
        if not match:
            await interaction.response.send_message("Please provide the old and new sound names in quotes. Example: !rename \"old name\" \"new name\"")
            return

        oldname, newname = match.groups()
        await sound_management.rename_sound(interaction, oldname, newname, SOUNDS_FOLDER, user_sound_mapping, PERSISTENCE_FILE)
        await create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID, SOUNDS_FOLDER)

    @tree.command(name="ytdlsound", description="Download and trim a sound from YouTube. -n name -l link -s start HH:MM:SS.sss -e end HH:MM:SS.sss")
    async def ytdlsound(interaction: discord.Interaction, *, args: str):
        args_dict = helper.parse_arguments(args, ['-n', '-l', '-s', '-e'])

        name = args_dict['-n']
        url = args_dict['-l']
        start = args_dict['-s']
        end = args_dict['-e']

        if not name or not url:
            await interaction.response.send_message("You must provide both a name and a YouTube URL.")
            return

        await interaction.response.send_message(f"Downloading sound from {url}...")
        try:
            output_file = os.path.join(SOUNDS_FOLDER, f"{name}")
            ydl_opts = {
                'format': 'bestaudio/best',  # Download best audio format
                'outtmpl': output_file,     # Save to SOUNDS_FOLDER with the provided name
                'noplaylist': True,         # Ensure only the single video is downloaded
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',   # Extract audio
                    'preferredcodec': 'mp3',      # Convert to MP3
                    'preferredquality': '192',    # Set quality to 192 kbps
                }],
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            

            if start or end:
                audio = AudioFileClip(f"{output_file}.mp3")
                start_seconds = helper.convert_to_seconds(start) if start else 0
                end_seconds = helper.convert_to_seconds(end) if end else audio.duration
                trimmed_audio = audio.subclip(start_seconds, end_seconds)
                trimmed_output_file = os.path.join(SOUNDS_FOLDER, f"{name}_trimmed.mp3")
                trimmed_audio.write_audiofile(trimmed_output_file)
                audio.close()
                os.remove(f"{output_file}.mp3")
                os.rename(trimmed_output_file, f"{output_file}.mp3")

            await interaction.followup.send(f"Sound '{name}' has been saved.")
            await create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID, SOUNDS_FOLDER)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")
    
    @tree.command(name="volume", description="Change the volume of a saved sound. -n name -m multiplier [-r to replace original]")
    async def volume(interaction: discord.Interaction, *, args: str):
        args_dict = helper.parse_arguments(args, ['-n', '-m', '-r'])

        name = args_dict.get('-n')
        multiplier = args_dict.get('-m')
        replace_original = '-r' in args_dict  # Check if the `-r` flag is present

        if not name or not multiplier:
            await interaction.response.send_message("You must provide both the sound name (-n) and a volume multiplier (-m).")
            return

        try:
            multiplier = float(multiplier)  # Convert multiplier to a float
            sound_file = os.path.join(SOUNDS_FOLDER, f"{name}.mp3")

            if not os.path.exists(sound_file):
                await interaction.response.send_message(f"The sound '{name}' does not exist.")
                return

            # Load the audio file
            audio = AudioFileClip(sound_file)

            # Apply the volume multiplier
            amplified_audio = audio.volumex(multiplier)

            # Define output file
            output_file = sound_file if replace_original else os.path.join(SOUNDS_FOLDER, f"{name}_volume_{multiplier:.1f}.mp3")

            # Save the amplified sound
            amplified_audio.write_audiofile(output_file, codec="mp3")
            audio.close()

            if replace_original:
                await interaction.response.send_message(f"The sound '{name}' has been amplified by a factor of {multiplier:.1f} and replaced.")
            else:
                await interaction.response.send_message(
                    f"The sound '{name}' has been amplified by a factor of {multiplier:.1f} and saved as '{name}_volume_{multiplier:.1f}.mp3'."
                )

            # Update the soundboard
            await create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID, SOUNDS_FOLDER)

        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")

    @tree.command()
    async def refresh(interaction: discord.Interaction):
        await create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID, SOUNDS_FOLDER)

async def create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID,SOUNDS_FOLDER):
    try:
        channel = bot.get_guild(GUILD_ID).get_channel(SOUNDBOARD_CHANNEL_ID)
        if channel:
            sb_view = soundboard_view.SoundboardView(SOUNDS_FOLDER, bot)
            for page in sb_view.pages:
                await channel.send(view=page)
        else:
            print(f"Soundboard channel with ID {SOUNDBOARD_CHANNEL_ID} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
