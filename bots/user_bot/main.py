import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import BOT_TOKEN_USER, REDIS_URL
from bots.user_bot.users.handlers import call_application, complaints, register, suggestion, settings, application_choise, usefull_contacts, chat
from bots.user_bot.middlewares import BlockCheckMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from bots.user_bot.admin.handlers import broadcast, user_management, questions
import redis.asyncio as redis


async def main():
    bot = Bot(token=BOT_TOKEN_USER)
    storage = RedisStorage.from_url(REDIS_URL)

    # # Create Redis connection
    # redis_client = redis.Redis(host="localhost", port=6379)

    # # Use RedisStorage for FSM
    # storage = RedisStorage(redis=redis_client)

    dp = Dispatcher(storage=storage)
    
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

    # admin routers
    dp.include_router(broadcast.router)
    dp.include_router(user_management.router)
    dp.include_router(questions.router)


    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
