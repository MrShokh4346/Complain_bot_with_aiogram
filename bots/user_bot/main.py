import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import BOT_TOKEN_USER
from bots.user_bot.handlers import call_application, complaints, register, suggestion, settings, application_choise, usefull_contacts
from bots.user_bot.middlewares import BlockCheckMiddleware


async def main():
    bot = Bot(token=BOT_TOKEN_USER)
    dp = Dispatcher(storage=MemoryStorage())
    
    # dp.message.middleware(BlockCheckMiddleware())

    dp.include_router(register.router)
    dp.include_router(complaints.router)
    dp.include_router(suggestion.router)
    dp.include_router(call_application.router)
    dp.include_router(settings.router)
    dp.include_router(application_choise.router)
    dp.include_router(usefull_contacts.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
