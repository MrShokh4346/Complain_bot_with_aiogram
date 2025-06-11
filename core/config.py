import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN_USER = os.getenv("BOT_TOKEN_USER")
BOT_TOKEN_ADMIN = os.getenv("BOT_TOKEN_ADMIN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))
COMPLAINT_GROUP_ID = int(os.getenv("COMPLAINT_GROUP_ID"))
CALLBACK_GROUP_ID = int(os.getenv("CALLBACK_GROUP_ID"))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

