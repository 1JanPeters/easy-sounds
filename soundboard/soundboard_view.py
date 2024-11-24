from discord.ui import Button, View
import discord
import soundboard.helper as helper


class SoundboardView(View):
    def __init__(self, SOUNDS_FOLDER, bot):
        super().__init__(timeout=None)
        self.SOUNDS_FOLDER = SOUNDS_FOLDER
        self.buttons_per_page = 20
        self.bot = bot
        self.pages = self.create_pages()

    def create_pages(self):
        keywords = helper.load_sounds(self.SOUNDS_FOLDER)
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[0].lower())  # Sorting case insensitively
        pages = []
        for i in range(0, len(sorted_keywords), self.buttons_per_page):
            buttons = sorted_keywords[i:i + self.buttons_per_page]
            page = self.create_page(buttons)
            pages.append(page)
        return pages

    def create_page(self, buttons):
        page = View(timeout=None)
        for word, sound_file in buttons:
            # Determine the style based on the first character of the sound name
            style = self.get_style_for_character(word[0].lower())
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

                await helper.play_sound(
                    sound_file=sound_file,
                    voice_channel=voice_channel,
                    SOUNDS_FOLDER=self.SOUNDS_FOLDER,
                    bot=self.bot
                )
            except Exception as e:
                print(f"Error playing sound via button: {e}")
        return callback

    @staticmethod
    def get_style_for_character(char):
        """
        Map the first character of the sound name to a Discord ButtonStyle.
        Iterates through ButtonStyles: PRIMARY, SECONDARY, SUCCESS, DANGER.
        """
        styles = [
            discord.ButtonStyle.primary,
            discord.ButtonStyle.secondary,
            discord.ButtonStyle.success,
            discord.ButtonStyle.danger
        ]
        index = (ord(char) - ord('a')) % len(styles)  # Wrap around if outside range
        return styles[index]