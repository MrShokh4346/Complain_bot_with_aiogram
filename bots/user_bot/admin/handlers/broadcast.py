from sqlalchemy import select
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.config import ADMIN_GROUP_ID
from db.crud.user_crud import get_all_users
from db.models import User
from db.base import async_session_maker

router = Router()
@router.message(F.text.startswith("/broadcast") & F.chat.id == ADMIN_GROUP_ID)
async def broadcast_command(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer("❗ Использование: `/broadcast `ваш текст", parse_mode="Markdown")
        return
    content = message.text[len("/broadcast "):]
    async with async_session_maker() as session:
        users = await session.execute(select(User.id))
        for row in users.scalars().all():
            try:
                await message.bot.send_message(chat_id=row, text=content)
            except Exception:
                pass  # user blocked bot or error occurred
    await message.answer("✅ Рассылка завершена.")
