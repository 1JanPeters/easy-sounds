import os
import discord
from moviepy.editor import AudioFileClip
from  soundboard.commands import create_soundboard

def register_events(bot, SOUNDS_FOLDER, GUILD_ID, SOUNDBOARD_CHANNEL_ID, user_sound_mapping):
    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel is None and after.channel is not None:
            if member.id in user_sound_mapping:
                sound_file = user_sound_mapping[member.id]
                voice_channel = after.channel
                voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
                if voice_client is None:
                    voice_client = await voice_channel.connect(self_deaf=True)
                elif voice_client.channel != voice_channel:
                    await voice_client.move_to(voice_channel)

                source = discord.FFmpegPCMAudio(os.path.join(SOUNDS_FOLDER, sound_file))
                voice_client.play(source)

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        await create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID, SOUNDS_FOLDER)
        await bot.tree.sync()

    @bot.event
    async def on_message(message):
        if message.channel.id == SOUNDBOARD_CHANNEL_ID and message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('audio'):
                    file_path = os.path.join(SOUNDS_FOLDER, attachment.filename)
                    mp3_path = os.path.splitext(file_path)[0] + '.mp3'

                    # Check if the file is already saved
                    if not os.path.exists(file_path):
                        await attachment.save(file_path)
                        await message.channel.send(f"File {attachment.filename} saved to sound folder.")
                        
                        # Convert to MP3 if it's not already in MP3 format
                        if not file_path.endswith('.mp3'):
                            try:
                                # Convert audio to MP3 using moviepy
                                audio_clip = AudioFileClip(file_path)
                                audio_clip.write_audiofile(mp3_path, codec='mp3')
                                audio_clip.close()

                                # Remove the original file if it wasn't MP3
                                os.remove(file_path)
                                await message.channel.send(f"File {attachment.filename} converted to MP3 and saved.")
                            except Exception as e:
                                await message.channel.send(f"An error occurred while converting the file: {e}")
                                print(f"Error converting audio: {e}")
                        else:
                            await message.channel.send(f"File is already in MP3 format.")

                        # Update soundboard (optional)
                        await create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID, SOUNDS_FOLDER)
                    else:
                        await message.channel.send(f"File {attachment.filename} already exists.")
                    break

        # Process other commands
        await bot.process_commands(message)
