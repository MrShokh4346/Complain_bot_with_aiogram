from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bots.user_bot.states import ContactCallState, ChatSupportState
from core.config import ADMIN_GROUP_ID

router = Router()

@router.message(F.text.lower().contains("связаться"))
async def contact_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📞 Перезвоните мне", callback_data="contact_call")
    builder.button(text="💬 Свяжитесь со мной в чат-боте", callback_data="contact_chat")
    builder.button(text="⬅️ Назад", callback_data="main_menu")
    await message.answer("Выберите способ связи из нижеперечисленного списка:", reply_markup=builder.as_markup())

# ----- CALL REQUEST -----
@router.callback_query(F.data == "contact_call")
async def ask_confirm_number(callback: CallbackQuery, state: FSMContext):
    # Assume phone is stored or hardcoded (later we fetch from DB)
    phone = "+79177220895"
    await state.set_state(ContactCallState.confirm)
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да", callback_data="call_confirm")
    builder.button(text="✏️ Оставить номер телефона", callback_data="call_change")
    await callback.message.answer(f"Это Ваш верный номер телефона {phone}?\nЕсли да, нажмите соответствующую кнопку, если нет, впишите свой актуальный номер телефона здесь:", reply_markup=builder.as_markup())

@router.callback_query(F.data == "call_confirm")
async def confirm_call(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user
    # Notify admin group
    await callback.bot.send_message(ADMIN_GROUP_ID, f"📞 Пользователь просит перезвонить:\n@{user.username or '—'} (id: {user.id})")
    await callback.message.answer("Отлично! Наш диспетчер перезвонит Вам в ближайшее время.")
    await state.clear()

@router.callback_query(F.data == "call_change")
async def wait_new_phone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ContactCallState.wait_phone)
    await callback.message.answer("Пожалуйста, введите Ваш актуальный номер телефона:")

@router.message(ContactCallState.wait_phone)
async def get_new_phone(message: Message, state: FSMContext):
    user = message.from_user
    phone = message.text
    await message.bot.send_message(ADMIN_GROUP_ID, f"📞 Пользователь просит перезвонить на номер: {phone}\n@{user.username or '—'} (id: {user.id})")
    await message.answer("Спасибо! Наш диспетчер перезвонит Вам в ближайшее время.")
    await state.clear()

# ----- CHAT WITH DISPATCHER -----
@router.callback_query(F.data == "contact_chat")
async def contact_chat_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChatSupportState.chat)
    builder = InlineKeyboardBuilder()
    builder.button(text="🛑 Диалог с администратором заканчивается", callback_data="end_chat")
    await callback.message.answer(
        'Добрый день! Я - диспетчер управляющей компании "УЭР-ЮГ", готов помочь Вам.\nНапишите, пожалуйста, интересующий Вас вопрос и ожидайте.',
        reply_markup=builder.as_markup()
    )

@router.message(ChatSupportState.chat)
async def relay_to_admin(message: Message):
    user = message.from_user
    await message.bot.send_message(ADMIN_GROUP_ID, f"💬 Новое сообщение от @{user.username or '—'} (id: {user.id}):\n{message.text}")

@router.callback_query(F.data == "end_chat")
async def end_chat(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Диалог завершен. Возвращаемся в главное меню.")
    await state.clear()
