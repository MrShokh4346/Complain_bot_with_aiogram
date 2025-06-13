import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import BOT_TOKEN_USER
from bots.user_bot.users.handlers import call_application, complaints, register, suggestion, settings, application_choise, usefull_contacts, chat
from bots.user_bot.middlewares import BlockCheckMiddleware, AdminCheckMiddleware

from bots.user_bot.admin.handlers import broadcast, user_management, questions


async def main():
    bot = Bot(token=BOT_TOKEN_USER)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(register.router)

    # Register and block middlewares
    dp.message.middleware(BlockCheckMiddleware())

    # user routers
    dp.include_router(call_application.router)
    dp.include_router(settings.router)
    dp.include_router(usefull_contacts.router)
    dp.include_router(suggestion.router)
    dp.include_router(chat.router)
    dp.include_router(application_choise.router)
    dp.include_router(complaints.router)

    # # admin middleware
    # broadcast.router.message.middleware(AdminCheckMiddleware())
    # commands.router.message.middleware(AdminCheckMiddleware())
    # user_management.router.message.middleware(AdminCheckMiddleware())
    # questions.router.message.middleware(AdminCheckMiddleware())
    
    # admin routers
    dp.include_router(broadcast.router)
    dp.include_router(user_management.router)
    dp.include_router(questions.router)


    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
