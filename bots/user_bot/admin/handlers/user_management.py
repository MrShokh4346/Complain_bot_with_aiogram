from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.config import ADMIN_GROUP_ID
from core.utils import make_user_info_text
from db.crud.user_crud import get_user_by_id, get_user_by_telegram_id_or_username, set_user_block_status

router = Router()


@router.message(
    Command("userinfo"),
    # F.chat.type.in_({"group", "supergroup"}),
    # F.chat.id == ADMIN_GROUP_ID
)
async def user_info(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer("❗ Укажите ID пользователя: `/userinfo <user_id>` или  `/userinfo <username>`", parse_mode="Markdown")
        return
    info = await make_user_info_text(parts)
    await message.answer(info)


# # Example: /questions
# @router.message(F.text == "/questions")
# async def list_questions(message: Message):
#     async with async_session_maker() as session:
#         questions = await session.execute(select(Question).where(Question.answered == False))
#         for q in questions.scalars().all():
#             await message.answer(
#                 f"❓ Вопрос от @{q.username}:\n\n{q.text}",
#                 reply_markup=InlineKeyboardMarkup(
#                     inline_keyboard=[
#                         [InlineKeyboardButton(text="Ответить", callback_data=f"answer_{q.id}")]
#                     ]
#                 )
#             )



# @router.message(F.text.startswith("/block") & F.chat.id == ADMIN_GROUP_ID)
# async def block_user(message: Message):
#     parts = message.text.split()
#     if len(parts) < 2:
#         return await message.answer("Используйте: /block <user_id>")

#     user_id = int(parts[1])
#     user = await get_user_by_id(user_id)
#     if user:
#         user.is_blocked = True
#         await save_user(user)
#         await message.answer(f"🚫 Пользователь {user_id} заблокирован.")
#     else:
#         await message.answer("Пользователь не найден.")
