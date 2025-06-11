from aiogram import Router
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
import re

router = Router()

@router.message(commands=["start"])
async def admin_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 Рассылка", callback_data="admin_broadcast")
    builder.button(text="🔍 Пользователи", callback_data="admin_users")
    builder.button(text="🚫 Блок/Разблок", callback_data="admin_block")
    builder.button(text="💬 Ответить на вопрос", callback_data="admin_reply")
    builder.button(text="📞 Заявки на звонок", callback_data="admin_calls")

    await message.answer(
        "Добро пожаловать в админ-панель 👮‍♂️\nВыберите действие:",
        reply_markup=builder.as_markup()
    )


@router.message(F.reply_to_message)
async def reply_to_user(message: Message):
    original_text = message.reply_to_message.text or message.reply_to_message.caption
    if not original_text:
        return

    # Extract user_id
    match = re.search(r"reply_to_user_id:(\d+)", original_text)
    if not match:
        await message.answer("❌ Не удалось определить получателя.")
        return

    user_id = int(match.group(1))
    try:
        if message.photo:
            await message.bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption or "")
        elif message.text:
            await message.bot.send_message(user_id, message.text)
        else:
            await message.answer("⚠️ Поддерживаются только текст и фото.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке сообщения пользователю: {e}")

