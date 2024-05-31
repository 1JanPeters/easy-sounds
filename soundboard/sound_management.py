import os
import soundboard.helper as helper 

async def delete_sound(interaction, sound_name, SOUNDS_FOLDER):
    sound_file = f"{sound_name}.mp3"
    sound_path = os.path.join(SOUNDS_FOLDER, sound_file)
    if not os.path.exists(sound_path):
        await interaction.response.send_message(f"Sound '{sound_name}' not found.")
        return

    os.remove(sound_path)
    await interaction.response.send_message(f"Sound '{sound_name}' has been deleted.")

async def rename_sound(interaction, oldname, newname, SOUNDS_FOLDER, user_sound_mapping, PERSISTENCE_FILE):
    old_sound_file = f"{oldname}.mp3"
    new_sound_file = f"{newname}.mp3"
    old_sound_path = os.path.join(SOUNDS_FOLDER, old_sound_file)
    new_sound_path = os.path.join(SOUNDS_FOLDER, new_sound_file)

    if not os.path.exists(old_sound_path):
        await interaction.response.send_message(f"Sound '{oldname}' not found.")
        return

    if os.path.exists(new_sound_path):
        await interaction.response.send_message(f"Sound '{newname}' already exists.")
        return

    os.rename(old_sound_path, new_sound_path)
    await interaction.response.send_message(f"Sound '{oldname}' has been renamed to '{newname}'.")

    for user, sound_file in user_sound_mapping.items():
        if sound_file == old_sound_file:
            user_sound_mapping[user] = new_sound_file
    helper.save_user_sound_mapping(PERSISTENCE_FILE, user_sound_mapping)
