🎵 Telegram VC Music Player Bot

A simple and efficient Voice Chat Music Player Bot for Telegram that can run 24/7 on Termux. Play lag-free music in your group voice chats with easy-to-use commands.
✨ Features

    🎶 High-quality audio streaming

    ⏯️ Play, Pause, Resume functionality

    📋 Song queue management

    🔍 YouTube search support

    🔗 Direct URL support

    ⏭️ Skip songs

    🛑 Stop and clear queue

    📱 Optimized for Termux

    🌐 24/7 operation support

🚀 Quick Start
Prerequisites

    Python 3.7+

    Termux app

    Telegram account

    Bot Token from @BotFather

Installation

    Update Termux and install dependencies:

bash

pkg update && pkg upgrade
pkg install python ffmpeg libopus

    Download the bot files and create required files:

    Install Python dependencies:

bash

pip install pyrogram tgcrypto python-dotenv pytgcalls youtube-dl yt-dlp requests aiohttp aiofiles

    Get Telegram API credentials:

        Visit my.telegram.org

        Create a new application

        Note down API_ID and API_HASH

    Create a bot with @BotFather:

        Start chat with @BotFather

        Use /newbot command

        Follow instructions and get your bot token

    Configure environment:
    Create a .env file:

env

API_ID=your_api_id_here
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here

🏃‍♂️ Running the Bot

Start the bot:
bash

python music_bot.py

For 24/7 operation in Termux:

Method 1: Using tmux
bash

pkg install tmux
tmux new -s musicbot
python music_bot.py
# Detach: Ctrl+B, then D
# Reattach: tmux attach -t musicbot

Method 2: Using nohup
bash

nohup python music_bot.py > bot.log 2>&1 &

Method 3: Auto-restart script
Create start_bot.sh:
bash

#!/bin/bash
while true; do
    python music_bot.py
    echo "Bot crashed! Restarting in 5 seconds..."
    sleep 5
done

Make executable and run:
bash

chmod +x start_bot.sh
./start_bot.sh

📋 Bot Commands
Command	Description
/start	Start the bot and show help
/play [song]	Play a song from YouTube
/pause	Pause current song
/resume	Resume paused song
/skip	Skip to next song
/queue	Show current queue
/end	Stop music and clear queue
🎯 Usage Examples

    Add bot to your group and make it admin

    Join voice chat in the group

    Play music:

        /play despacito - Search and play

        /play https://youtu.be/example - Play from URL

    Control playback:

        /pause - Pause music

        /resume - Resume music

        /skip - Skip current song

        /queue - Check what's playing next

🛠️ Project Structure
text

telegram-vc-music-bot/
├── music_bot.py      # Main bot code
├── requirements.txt  # Python dependencies
├── .env             # Environment variables
├── start_bot.sh     # Auto-restart script
└── README.md        # This file

🔧 Configuration
Environment Variables
Variable	Description	Required
API_ID	Telegram API ID	Yes
API_HASH	Telegram API Hash	Yes
BOT_TOKEN	Bot token from @BotFather	Yes
Bot Permissions

Make sure your bot has these permissions in the group:

    ✅ Delete messages

    ✅ Manage voice chats

    ✅ Invite users

    ✅ Pin messages

🐛 Troubleshooting
Common Issues

    Bot can't join voice chat:

        Ensure bot has admin permissions

        Check if voice chat is active

    No audio playback:

        Verify FFmpeg installation: ffmpeg -version

        Check internet connection

    Bot crashes frequently:

        Check logs for error messages

        Ensure all dependencies are installed

    YouTube videos not playing:

        Update youtube-dl: pip install --upgrade yt-dlp

        Check if video is region-restricted

Logs and Debugging

    Check application logs in console

    For nohup: tail -f nohup.out

    Enable debug logging by modifying the Python code

📝 Dependencies
System Dependencies

    Python 3.7+

    FFmpeg

    libopus

Python Dependencies

    Pyrogram - Telegram MTProto API

    PyTgCalls - Telegram voice calls

    youtube-dl/yt-dlp - YouTube audio extraction

    python-dotenv - Environment management

🤝 Contributing

Feel free to contribute to this project by:

    Reporting bugs

    Suggesting new features

    Submitting pull requests

📄 License

This project is open source and available under the MIT License.
⚠️ Disclaimer

This bot is for educational purposes. Make sure to comply with:

    Telegram's Terms of Service

    YouTube's Terms of Service

    Copyright laws in your country

📞 Support

If you need help setting up the bot:

    Check this README thoroughly

    Look at existing issues

    Create a new issue with detailed description

Enjoy your music! 🎧
