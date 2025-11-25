```bash
#!/bin/bash

# Telegram VC Music Bot - Auto Restart Script
# This script keeps the bot running 24/7 and automatically restarts if it crashes

echo "Starting Telegram VC Music Bot..."
echo "Press Ctrl+C to stop the bot completely"

# Function to handle cleanup
cleanup() {
    echo ""
    echo "Stopping bot..."
    pkill -f "python music_bot.py"
    exit 0
}

# Set trap for Ctrl+C
trap cleanup SIGINT

# Infinite loop to restart bot if it crashes
while true; do
    echo "$(date): Starting bot..."
    python music_bot.py
    
    # If the bot exits/crashes
    echo "$(date): Bot stopped/crashed. Restarting in 5 seconds..."
    sleep 5
    
    # Clear any residual processes
    pkill -f "ffmpeg" 2>/dev/null || true
    sleep 1
done
