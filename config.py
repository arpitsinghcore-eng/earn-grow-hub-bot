import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    "8748410522:AAEUdKurcknTCfPostY0TEHDnEmlSe66gEs"
)

# Admin Telegram ID
ADMIN_ID = int(os.getenv("ADMIN_ID", "8532790017"))

# Currency
CURRENCY = "₹"

# Rewards
GMAIL_REWARD = 6
REVIEW_REWARD = 2
REFERRAL_BONUS = 2

# Withdraw Settings
MIN_WITHDRAW = 50
MAX_DAILY_WITHDRAW = 5

# Force Join
CHANNEL_USERNAME = "@earn_growhub3"
GROUP_USERNAME = "@earn_growhub"

# Bot Name
BOT_NAME = "Earn Grow Hub"