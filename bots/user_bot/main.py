import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.redis_client import redis_client
from core.config import BOT_TOKEN_USER, REDIS_URL
from bots.user_bot.users.handlers import call_application, complaints, register, suggestion, settings, application_choise, usefull_contacts, chat
from bots.user_bot.middlewares import BlockCheckMiddleware, CheckRegistrationMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from bots.user_bot.admin.handlers import broadcast, user_management, questions

def apply_middlewares(router):
    router.message.middleware(CheckRegistrationMiddleware())
    router.message.middleware(BlockCheckMiddleware())


async def main():
    bot = Bot(token=BOT_TOKEN_USER)
    storage = RedisStorage(redis=redis_client)

    dp = Dispatcher(storage=storage)
    
    dp.include_router(register.router)

    # Register and block middlewares
    for router in [
        call_application.router,
        settings.router,
        usefull_contacts.router,
        suggestion.router,
        chat.router,
        application_choise.router,
        complaints.router
    ]:
        apply_middlewares(router)

    # user routers
    dp.include_router(call_application.router)
    dp.include_router(settings.router)
    dp.include_router(usefull_contacts.router)
    dp.include_router(suggestion.router)
    dp.include_router(chat.router)
    dp.include_router(application_choise.router)
    dp.include_router(complaints.router)

    # admin routers
    dp.include_router(broadcast.router)
    dp.include_router(user_management.router)
    dp.include_router(questions.router)


    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
