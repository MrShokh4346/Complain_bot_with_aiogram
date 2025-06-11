from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bots.common.texts import Texts
from bots.user_bot.keyboards.main_menu import main_menu_keyboard
from bots.user_bot.keyboards.settings import settings_navigation_buttons
from bots.user_bot.states import SettingsState
from core.utils import is_valid_cyrillic_name
from db.crud import add_or_update_user


router = Router()


@router.message(F.text.lower().contains("настройки"))
async def settings_menu(message: Message, state: FSMContext):
    await message.answer(Texts.get_settings_text(), reply_markup=settings_navigation_buttons())


@router.callback_query(F.data == "settings_change_name")
async def ask_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SettingsState.set_name)
    await callback.message.answer("🛠 Отправьте своё Имя и Фамилию, чтобы поменять настройки:")


@router.message(SettingsState.set_name)
async def save_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if is_valid_cyrillic_name(message.text):
        await add_or_update_user(user_id, full_name=message.text)
        await message.answer("🛠✅🛠 Настройки имени успешно применены", reply_markup=main_menu_keyboard())
        await state.clear()
        return
    await message.answer("❗ Пожалуйста, введите корректное Имя и Фамилию (например: Иван Иванов).")


@router.callback_query(F.data == "settings_change_phone")
async def ask_phone(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SettingsState.set_phone)
    await callback.message.answer("🛠 Отправьте свой номер телефона, чтобы поменять настройки:")


@router.message(SettingsState.set_phone)
async def save_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not message.text.startswith("+7") or len(message.text) != 12 or not message.text[2:].isdigit():
        await message.answer("❗ Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX.")
        return
    await add_or_update_user(user_id, phone_number=message.text)
    await message.answer("🛠✅🛠 Настройки номера успешно применены", reply_markup=main_menu_keyboard())
    await state.clear()


@router.callback_query(F.data == "settings_back")
async def settings_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(Texts.get_main_menu_text())