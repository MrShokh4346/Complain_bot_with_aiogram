from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bots.common.texts import Texts
from bots.user_bot.users.keyboards.call_application import answer_question_directly_navigation_buttons, end_chat_navigation_buttons
from bots.user_bot.users.keyboards.main_menu import main_menu_keyboard
from bots.user_bot.states import  ChatSupportState
from core.config import ADMIN_GROUP_ID, COMPLAINT_GROUP_ID
from core.utils import save_question
from db.crud.user_crud import get_user_by_id

router = Router()


# ----- CHAT WITH DISPATCHER -----
@router.callback_query(F.data == "contact_chat")
async def contact_chat_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ChatSupportState.chat)
    await callback.message.answer(Texts.get_chat_support_text(), reply_markup=end_chat_navigation_buttons())


@router.message(ChatSupportState.chat)
async def relay_to_admin(message: Message):
    user_id = message.from_user.id
    user = await get_user_by_id(user_id)
    question_text, question_id = await save_question(message.text, user_id)
    if not user:
        await message.answer("Пользователь не найден. Пожалуйста, попробуйте позже.")
        return
    await message.bot.send_message(COMPLAINT_GROUP_ID, question_text, reply_markup=answer_question_directly_navigation_buttons(question_id))


@router.callback_query(F.data == "end_chat")
async def end_chat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("❌📞 Диалог с администраторам завершён...", reply_markup=main_menu_keyboard())
    await state.clear()
