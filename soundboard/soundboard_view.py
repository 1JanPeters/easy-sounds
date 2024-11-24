import hashlib
from discord.ui import Button, View
import discord
import soundboard.helper as helper


class SoundboardView(View):
    def __init__(self, SOUNDS_FOLDER, bot):
        super().__init__(timeout=None)
        self.SOUNDS_FOLDER = SOUNDS_FOLDER
        self.buttons_per_page = 20
        self.pages = self.create_pages()
        self.bot = bot

    def create_pages(self):
        keywords = helper.load_sounds(self.SOUNDS_FOLDER)
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[0].lower())  # Sorting case insensitively
        pages = []
        for i in range(0, len(sorted_keywords), self.buttons_per_page):
            buttons = sorted_keywords[i:i+self.buttons_per_page]
            page = self.create_page(buttons)
            pages.append(page)
        return pages

    def create_page(self, buttons):
        page = View(timeout=None)
        for word, sound_file in buttons:
            # Determine the color for the button based on the sound file name
            style = self.get_style_for_sound(sound_file)
            button = Button(label=word, style=style)
            button.callback = self.create_sound_callback(sound_file)
            page.add_item(button)
        return page

    def create_sound_callback(self, sound_file):
        async def callback(interaction: discord.Interaction):
            try:
                await interaction.response.defer()
                author = interaction.user
                voice_state = author.voice
                
                if voice_state is None or voice_state.channel is None:
                    await interaction.followup.send("You are not in a voice channel.", ephemeral=True)
                    return
                voice_channel = voice_state.channel
                
                await helper.play_sound(sound_file=sound_file, voice_channel=voice_channel, SOUNDS_FOLDER=self.SOUNDS_FOLDER, bot=self.bot)
            except Exception as e:
                print(f"Error playing sound via button: {e}")
        return callback

    def get_style_for_sound(self, sound_file):
        """
        Determine the button style (color) based on the hash of the sound file name.
        """
        # Generate a hash of the sound file name
        hash_value = int(hashlib.md5(sound_file.encode()).hexdigest(), 16)
        
        # Map the hash value to one of the available styles
        styles = [
            discord.ButtonStyle.primary,   # Blue
            discord.ButtonStyle.secondary, # Grey
            discord.ButtonStyle.success,   # Green
            discord.ButtonStyle.danger     # Red
        ]
        return styles[hash_value % len(styles)]