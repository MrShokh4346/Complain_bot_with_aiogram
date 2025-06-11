import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import BOT_TOKEN_USER
from bots.user_bot.handlers import complaints, register, suggestion, contact, settings, application_choise
from bots.user_bot.middlewares import BlockCheckMiddleware


async def main():
    bot = Bot(token=BOT_TOKEN_USER)
    dp = Dispatcher(storage=MemoryStorage())
    
    # dp.message.middleware(BlockCheckMiddleware())

    dp.include_router(register.router)
    dp.include_router(complaints.router)
    dp.include_router(suggestion.router)
    dp.include_router(contact.router)
    dp.include_router(settings.router)
    dp.include_router(application_choise.router)

    from aiogram import Router, F
    from aiogram.types import Message, CallbackQuery, FSInputFile
    from aiogram.fsm.context import FSMContext
    
    # @dp.message(F.photo | F.video)
    # async def get_media(message: Message, state: FSMContext):
    #     data = await state.get_data()
    #     await state.update_data(media=message.photo[-1].file_id if message.photo else (message.video.file_id if message.video else None))
    #     await message.answer("Опишите суть проблемы:")



    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
