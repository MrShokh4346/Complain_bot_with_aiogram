from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bots.common.texts import Texts
from bots.user_bot.keyboards.call_application import call_application_navigation_buttons, call_request_navigation_buttons, end_chat_navigation_buttons
from bots.user_bot.keyboards.main_menu import main_menu_keyboard
from bots.user_bot.states import ContactCallState, ChatSupportState
from core.config import ADMIN_GROUP_ID, CALLBACK_GROUP_ID
from core.utils import make_callback_application
from db.crud import get_user_by_id

router = Router()

@router.message(F.text.lower().contains("связаться"))
async def contact_start(message: Message):
    await message.answer("👇 Выберите способ связи из нижеперечисленного списка:", reply_markup=call_application_navigation_buttons())

# ----- CALL REQUEST -----
@router.callback_query(F.data == "contact_call")
async def ask_confirm_number(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # Assume phone is stored or hardcoded (later we fetch from DB)
    user_id = callback.from_user.id
    user = await get_user_by_id(user_id)
    if not user:
        await callback.message.answer("Пользователь не найден. Пожалуйста, попробуйте позже.")
        return
    await state.set_state(ContactCallState.confirm)
    await callback.message.answer(f"Это Ваш верный номер телефона {user.phone_number}?\nЕсли да, нажмите соответствующую кнопку, если нет, впишите свой актуальный номер телефона здесь:", reply_markup=call_request_navigation_buttons())


@router.callback_query(F.data == "call_confirm")
async def confirm_call(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    user = await get_user_by_id(user_id)
    data = {'user': user}
    await callback.bot.send_message(CALLBACK_GROUP_ID, make_callback_application(data), parse_mode="HTML")
    await callback.message.answer("Отлично! Наш диспетчер перезвонит Вам в ближайшее время.")
    await state.clear()


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
    if not user:
        await message.answer("Пользователь не найден. Пожалуйста, попробуйте позже.")
        return
    await message.bot.send_message(CALLBACK_GROUP_ID, f"💬 Новое сообщение от @{user.username or '—'} ({user.full_name}):\n{message.text}")


@router.callback_query(F.data == "end_chat")
async def end_chat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("❌📞 Диалог с администраторам завершён...", reply_markup=main_menu_keyboard())
    await state.clear()
