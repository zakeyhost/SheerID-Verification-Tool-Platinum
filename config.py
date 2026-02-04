"""
Configuration settings for SheerID Verification Bot
"""
import os

# Telegram Bot Token (Replace with your token from @BotFather)
BOT_TOKEN = "7840853625:AAHoX1eNG1XDeBmDA9MYG9_5hW8pjYvaHqM"

# SheerID API Settings
SHEERID_API_URL = "https://services.sheerid.com/rest/v2"
REFERRER_URL = "https://verify.sheerid.com/"

# Connection Settings
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30  # seconds

# Verification Settings
AGE_MIN = 18
AGE_MAX = 24
COUNTRY = "US"

# Anti-Detect Settings
USE_PROXY = True
PROXY_URL = "http://jxbtrlti:42fcoicerjtv@23.26.71.145:5628"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "bot_activity.log"
