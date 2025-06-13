import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN_USER = os.getenv("BOT_TOKEN_USER")
BOT_TOKEN_ADMIN = os.getenv("BOT_TOKEN_ADMIN")

ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))
COMPLAINT_GROUP_ID = int(os.getenv("COMPLAINT_GROUP_ID"))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")

