import os
import discord
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
                    if not os.path.exists(file_path):
                        await attachment.save(file_path)
                        await message.channel.send(f"File {attachment.filename} saved to sound folder.")
                        await create_soundboard(bot, GUILD_ID, SOUNDBOARD_CHANNEL_ID, SOUNDS_FOLDER)
                    else:
                        await message.channel.send(f"File {attachment.filename} already exists.")
                    break

        await bot.process_commands(message)
