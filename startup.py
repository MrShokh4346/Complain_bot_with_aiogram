import asyncio
import os
from bots.user_bot.main import main
from scripts.init_db import init_models


if __name__ == "__main__":
    if not os.path.exists("bot_db.sqlite3"):
        print("Creating database...")
        asyncio.run(init_models())
        print("Done.")
    print("Starting bot...")
    asyncio.run(main())