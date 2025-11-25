import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
from youtube_dl import YoutubeDL
import requests
import json
from collections import deque
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("Please set API_ID, API_HASH, and BOT_TOKEN environment variables")

# Initialize clients
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

# Global variables
queues = {}
current_song = {}

# YouTube DL configuration
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

def search_yt(query):
    """Search YouTube and return audio URL"""
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in info:
                info = info['entries'][0]
            return {
                'url': info['url'],
                'title': info['title'],
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', '')
            }
    except Exception as e:
        logger.error(f"Error searching YouTube: {e}")
        return None

def get_audio_url(query):
    """Get audio URL from query"""
    if query.startswith('http'):
        # Direct URL
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                return {
                    'url': info['url'],
                    'title': info['title'],
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', '')
                }
        except Exception as e:
            logger.error(f"Error processing URL: {e}")
            return None
    else:
        # Search query
        return search_yt(query)

async def play_next(chat_id):
    """Play next song in queue"""
    if chat_id in queues and queues[chat_id]:
        song = queues[chat_id].popleft()
        current_song[chat_id] = song
        
        try:
            await pytgcalls.join_group_call(
                chat_id,
                AudioPiped(
                    song['url'],
                    HighQualityAudio(),
                )
            )
            await app.send_message(
                chat_id,
                f"🎵 **Now Playing:** {song['title']}\n⏱ Duration: {song['duration']}s"
            )
        except Exception as e:
            logger.error(f"Error playing song: {e}")
            await app.send_message(chat_id, "❌ Error playing song")
            # Try next song
            await play_next(chat_id)
    else:
        # No more songs in queue
        if chat_id in current_song:
            del current_song[chat_id]
        await app.send_message(chat_id, "✅ Queue finished")

# Command handlers
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    """Start command handler"""
    await message.reply_text(
        "🎵 **Music Bot Started!**\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/play [song] - Play a song\n"
        "/pause - Pause the song\n"
        "/resume - Resume the song\n"
        "/skip - Skip current song\n"
        "/queue - Show queue list\n"
        "/end - Stop music and clear queue"
    )

@app.on_message(filters.command("play"))
async def play_command(client, message: Message):
    """Play music command"""
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a song name or YouTube URL")
        return
    
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    
    # Check if user is in voice chat
    if not await is_user_in_voice_chat(client, message):
        await message.reply_text("❌ Please join a voice chat first!")
        return
    
    # Send searching message
    search_msg = await message.reply_text("🔍 Searching...")
    
    # Get audio URL
    song_info = get_audio_url(query)
    if not song_info:
        await search_msg.edit_text("❌ No results found")
        return
    
    await search_msg.edit_text(f"✅ Found: {song_info['title']}")
    
    # Initialize queue if not exists
    if chat_id not in queues:
        queues[chat_id] = deque()
    
    # Add to queue
    queues[chat_id].append(song_info)
    
    # If nothing is playing, start playing
    if chat_id not in current_song:
        await play_next(chat_id)
    else:
        await message.reply_text(f"✅ Added to queue: {song_info['title']}")

@app.on_message(filters.command("pause"))
async def pause_command(client, message: Message):
    """Pause command"""
    chat_id = message.chat.id
    try:
        await pytgcalls.pause_stream(chat_id)
        await message.reply_text("⏸️ Music paused")
    except Exception as e:
        await message.reply_text("❌ No music is playing or already paused")

@app.on_message(filters.command("resume"))
async def resume_command(client, message: Message):
    """Resume command"""
    chat_id = message.chat.id
    try:
        await pytgcalls.resume_stream(chat_id)
        await message.reply_text("▶️ Music resumed")
    except Exception as e:
        await message.reply_text("❌ No music is paused")

@app.on_message(filters.command("skip"))
async def skip_command(client, message: Message):
    """Skip command"""
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏭️ Skipped current song")
        await asyncio.sleep(1)
        await play_next(chat_id)
    except Exception as e:
        await message.reply_text("❌ No music is playing")

@app.on_message(filters.command("queue"))
async def queue_command(client, message: Message):
    """Queue command"""
    chat_id = message.chat.id
    
    if chat_id not in queues or not queues[chat_id]:
        await message.reply_text("📭 Queue is empty")
        return
    
    queue_text = "📋 **Queue:**\n\n"
    
    # Current playing song
    if chat_id in current_song:
        queue_text += f"🎵 **Now Playing:** {current_song[chat_id]['title']}\n\n"
    
    # Upcoming songs
    for i, song in enumerate(queues[chat_id], 1):
        queue_text += f"{i}. {song['title']}\n"
    
    await message.reply_text(queue_text)

@app.on_message(filters.command("end"))
async def end_command(client, message: Message):
    """End command"""
    chat_id = message.chat.id
    
    try:
        await pytgcalls.leave_group_call(chat_id)
    except:
        pass
    
    # Clear queue
    if chat_id in queues:
        queues[chat_id].clear()
    
    if chat_id in current_song:
        del current_song[chat_id]
    
    await message.reply_text("🛑 Music stopped and queue cleared")

async def is_user_in_voice_chat(client, message):
    """Check if user is in voice chat"""
    try:
        chat_id = message.chat.id
        member = await client.get_chat_member(chat_id, message.from_user.id)
        return member.status in ['creator', 'administrator', 'member']
    except:
        return False

# Event handlers
@pytgcalls.on_stream_end()
async def on_stream_end(chat_id: int):
    """Handle stream end"""
    logger.info(f"Stream ended in chat {chat_id}")
    await play_next(chat_id)

@pytgcalls.on_closed_voice_chat()
async def on_closed_voice_chat(chat_id: int):
    """Handle voice chat closed"""
    logger.info(f"Voice chat closed in {chat_id}")
    if chat_id in queues:
        queues[chat_id].clear()
    if chat_id in current_song:
        del current_song[chat_id]

# Main function
async def main():
    """Main function"""
    await pytgcalls.start()
    logger.info("Bot started successfully!")
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
