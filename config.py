"""
Configuration settings for SheerID Verification Bot
"""
import os

# Telegram Bot Token (Replace with your token from @BotFather)
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

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
USE_PROXY = False  # Set to True if you have proxies
PROXY_URL = ""     # Format: http://user:pass@host:port

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "bot_activity.log"
