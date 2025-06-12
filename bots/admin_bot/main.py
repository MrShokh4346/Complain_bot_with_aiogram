import asyncio
from aiogram import Bot, Dispatcher
from bots.user_bot.admin.handler import commands
from bots.admin_bot.middlewares import AdminCheckMiddleware
from bots.user_bot.admin.handler import broadcast
from bots.user_bot.admin.handler import user_management
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import BOT_TOKEN_ADMIN


async def main():
    bot = Bot(token=BOT_TOKEN_ADMIN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # dp.message.middleware(AdminCheckMiddleware())

    dp.include_router(broadcast.router)
    dp.include_router(commands.router)
    dp.include_router(user_management.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
