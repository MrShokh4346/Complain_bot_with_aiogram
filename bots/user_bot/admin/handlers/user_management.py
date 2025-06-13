from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.config import ADMIN_GROUP_ID
from core.utils import make_user_info_text
from db.crud.user_crud import unblock_user, block_user

router = Router()


@router.message(
    Command("userinfo"),
    F.chat.type.in_({"group", "supergroup"}),
    F.chat.id == ADMIN_GROUP_ID
)
async def user_info(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer("❗ Укажите ID или username пользователя: `/userinfo <user_id>` или  `/userinfo <username>`", parse_mode="Markdown")
        return
    info = await make_user_info_text(parts)
    await message.answer(info)


@router.message(
    Command("block"),
    F.chat.type.in_({"group", "supergroup"}),
    F.chat.id == ADMIN_GROUP_ID
)
async def block_user_function(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("❗ Укажите ID или username пользователя: `/block <user_id>` или  `/block <username>`")

    query = parts[1]
    result = await block_user(query)
    if result:
        await message.answer(f"🚫 Пользователь {query} заблокирован.")
    else:
        await message.answer("Пользователь не найден.")


@router.message(
    Command("unblock"),
    F.chat.type.in_({"group", "supergroup"}),
    F.chat.id == ADMIN_GROUP_ID
)
async def unblock_user_function(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("❗ Укажите ID или username пользователя: `/unblock <user_id>` или  `/unblock <username>`")

    query = parts[1]
    result = await unblock_user(query)
    if result:
        await message.answer(f"🚫 Пользователь {query} разблокирован.")
    else:
        await message.answer("Пользователь не найден.")
