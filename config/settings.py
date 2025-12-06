import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

# Football Data API
FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")

# Database
DB_NAME = "antigravity.db"
DB_PATH = os.path.join(os.getcwd(), DB_NAME)

# Scheduling
UPDATE_TIME = "08:00" # Daily update time
