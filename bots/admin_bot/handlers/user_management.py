from aiogram import Router
from aiogram.types import Message
from db.crud import get_user_by_telegram_id_or_username, set_user_block_status

router = Router()

@router.message(lambda msg: msg.text.startswith("/userinfo"))
async def user_info_handler(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        await message.answer("❗ Используйте команду так: /userinfo <id или username>")
        return

    query = parts[1].lstrip("@")  # remove @ if provided

    user = await get_user_by_telegram_id_or_username(query)
    if not user:
        await message.answer("Пользователь не найден.")
        return

    text = (
        f"<b>Информация о пользователе</b>\n"
        f"👤 ФИО: {user.full_name}\n"
        f"📞 Телефон: {user.phone}\n"
        f"🆔 Telegram ID: <code>{user.id}</code>\n"
        f"🔒 Заблокирован: {'Да' if user.is_blocked else 'Нет'}"
    )
    await message.answer(text)


@router.message(lambda msg: msg.text.startswith("/block"))
async def block_user(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        await message.answer("❗ Используйте: /block <id или username>")
        return

    query = parts[1].lstrip("@")
    success = await set_user_block_status(query, True)
    if success:
        await message.answer("✅ Пользователь заблокирован.")
    else:
        await message.answer("❌ Пользователь не найден.")

@router.message(lambda msg: msg.text.startswith("/unblock"))
async def unblock_user(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        await message.answer("❗ Используйте: /unblock <id или username>")
        return

    query = parts[1].lstrip("@")
    success = await set_user_block_status(query, False)
    if success:
        await message.answer("✅ Пользователь разблокирован.")
    else:
        await message.answer("❌ Пользователь не найден.")