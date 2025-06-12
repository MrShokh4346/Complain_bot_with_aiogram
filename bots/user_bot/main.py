import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import BOT_TOKEN_USER
from bots.user_bot.users.handlers import call_application, complaints, register, suggestion, settings, application_choise, usefull_contacts, chat
from bots.user_bot.middlewares import BlockCheckMiddleware

from bots.user_bot.admin.handlers import commands, broadcast, user_management, questions
from bots.admin_bot.middlewares import AdminCheckMiddleware


async def main():
    bot = Bot(token=BOT_TOKEN_USER)
    dp = Dispatcher(storage=MemoryStorage())
    
    # dp.message.middleware(BlockCheckMiddleware())

    # admin routers
    dp.include_router(broadcast.router)
    dp.include_router(commands.router)
    dp.include_router(user_management.router)
    dp.include_router(questions.router)

    # user routers
    dp.include_router(register.router)
    dp.include_router(complaints.router)
    dp.include_router(suggestion.router)
    dp.include_router(call_application.router)
    dp.include_router(chat.router)
    dp.include_router(settings.router)
    dp.include_router(application_choise.router)
    dp.include_router(usefull_contacts.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
