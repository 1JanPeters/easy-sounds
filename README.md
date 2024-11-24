# Easy-Sounds Bot

Easy-Sounds Bot is a powerful Discord bot that allows users to set join sounds, delete sounds, rename sounds, and download and trim sounds from YouTube all from a text channel for a custom soundboard experience.

## Features

- **Easy-to-Use Soundboard**: Sounds are displayed as buttons in the designated channel, making it very easy to play sounds with a single click.
- **Set Join Sound**: Users can set a custom sound to play when they join a voice channel.
- **Delete Sound**: Administrators can delete sound files from the soundboard.
- **Rename Sound**: Administrators can rename sound files.
- **Download and Trim from YouTube**: Users can download and trim sounds from YouTube.
- **Upload Sounds Directly**: Users can upload sound files directly to the designated text channel to add them to the soundboard.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/1JanPeters/easy-sounds.git
    cd easy-sounds
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Install `ffmpeg`:
    - On **Linux** (Debian-based systems like Ubuntu):
        ```sh
        sudo apt update
        sudo apt install ffmpeg
        ```
    - On **macOS** (using Homebrew):
        ```sh
        brew install ffmpeg
        ```
    - On **Windows**:
        - Download `ffmpeg` from [ffmpeg.org](https://ffmpeg.org/download.html).
        - Extract the files and add the `bin` directory to your system's PATH. (Refer to [this guide](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/) for detailed instructions.)

4. Copy the configuration template:
    - Copy `config_template.json` and save it as `config.json`.
    - Edit `config.json` and replace placeholders with your Discord bot token, guild ID, soundboard channel ID, and the full path to your sounds folder (e.g., `/home/user/sounds`, `C:\Users\user\sounds`).


## Requirements

- `discord.py==2.3.2`
- `moviepy==1.0.3`
- `pynacl`
- `yt-dlp`
- **ffmpeg** (must be installed on your system)


## Creating and Setting Up the Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).

2. Click on "New Application" and give it a name.

3. Navigate to the "Bot" section on the left sidebar and click on "Add Bot". Confirm by clicking "Yes, do it!".

4. Under the "TOKEN" section, click "Copy" to copy your bot token. This will be used in your `config.json` file.

5. Enable the "MESSAGE CONTENT INTENT" in the "Privileged Gateway Intents" section.

6. Retrieve your `APPLICATION_ID`:
    - On the "General Information" page of your application, copy the "Application ID".

7. Generate your bot's invite link:
    - Use the following URL format, replacing `APPLICATION_ID` with your application's ID:
      ```
      https://discord.com/oauth2/authorize?client_id=APPLICATION_ID&scope=bot&permissions=2150632448
      ```
    - Paste the generated URL into your browser, and invite the bot to your server.

8. Retrieve your `GUILD_ID`:
    - Right-click on your server icon in Discord.
    - Click on "Copy ID".

9. Create a text channel in your server for the soundboard and retrieve the `SOUNDBOARD_CHANNEL_ID`:
    - Right-click on the channel name.
    - Click on "Copy ID".

10. Update your `config.json` file with the `TOKEN`, `GUILD_ID`, and `SOUNDBOARD_CHANNEL_ID`.

## Usage

1. Run the bot:
    ```sh
    python bot.py
    ```

2. Use the following commands in Discord:
    - `/setjoinsound sound_name`: Set a sound to play when you join a voice channel.
    - `/deletesound sound_name`: Delete a sound file from the soundboard (admin only).
    - `/rename "old" "new"`: Rename a sound file (admin only).
    - `/ytdlsound -n name -l link -s start HH:MM:SS.sss -e end HH:MM:SS.sss`: Download and trim a sound from YouTube. The `-s` (start) and `-e` (end) parameters are optional. If not provided, the entire audio will be used as the sound.

3. Upload sound files directly to the soundboard:
    - Drag and drop your audio files (e.g., `.mp3`, `.wav`) into the designated text channel to add them to the soundboard.

## Disclaimer

This bot allows users to download and trim audio from YouTube. Users are responsible for ensuring they have the right to download and use the content in accordance with YouTube's [Terms of Service](https://www.youtube.com/static?template=terms). The developers of this bot are not responsible for any misuse of the tool.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Libraries

- `yt-dlp` is licensed under the [The Unlicense](https://opensource.org/licenses/Unlicense).
- `discord.py` and `moviepy` are licensed under the [MIT License](https://opensource.org/licenses/MIT).
- `pynacl` is licensed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).