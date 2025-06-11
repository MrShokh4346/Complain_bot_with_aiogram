from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bots.user_bot.states import SettingsState

# For now, store in-memory (replace with DB later)
USER_DATA = {}

router = Router()

@router.message(F.text.lower().contains("настройки"))
async def settings_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    profile = USER_DATA.get(user_id, {"name": "—", "phone": "—"})

    text = (
        f"🛠 Ваши текущие данные:\n"
        f"👤 ФИО: {profile['name']}\n"
        f"📞 Телефон: {profile['phone']}\n\n"
        "Что вы хотите изменить?"
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Изменить ФИО", callback_data="settings_change_name")
    builder.button(text="📱 Изменить номер телефона", callback_data="settings_change_phone")
    builder.button(text="⬅️ Назад", callback_data="main_menu")

    await state.set_state(SettingsState.choose)
    await message.answer(text, reply_markup=builder.as_markup())

@router.callback_query(F.data == "settings_change_name")
async def ask_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsState.set_name)
    await callback.message.answer("Пожалуйста, введите Ваше полное имя:")

@router.message(SettingsState.set_name)
async def save_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    USER_DATA.setdefault(user_id, {})["name"] = message.text
    await message.answer("ФИО успешно обновлено ✅")
    await state.clear()

@router.callback_query(F.data == "settings_change_phone")
async def ask_phone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsState.set_phone)
    await callback.message.answer("Пожалуйста, введите Ваш номер телефона:")

@router.message(SettingsState.set_phone)
async def save_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    USER_DATA.setdefault(user_id, {})["phone"] = message.text
    await message.answer("Номер телефона успешно обновлён ✅")
    await state.clear()
