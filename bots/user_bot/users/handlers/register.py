from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bots.common.texts import Texts
from bots.user_bot.users.keyboards.main_menu import main_menu_keyboard
from bots.user_bot.states import RegistrationState
from core.utils import is_valid_cyrillic_name
from db.crud.user_crud import add_or_update_user, get_user_by_telegram_id_or_username

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    # Check if user exists in the database
    user = await get_user_by_telegram_id_or_username(str(user_id))
    if user:
        # If user exists, check if they are blocked
        if user.is_blocked:
            await message.answer("🚫 Вы были заблокированы и не можете пользоваться ботом.")
            return
        await message.answer(Texts.get_main_menu_text(), reply_markup=main_menu_keyboard())
        return
    await state.set_state(RegistrationState.full_name)
    await message.answer(Texts.get_registration_text())


@router.message(RegistrationState.full_name)
async def get_full_name(message: Message, state: FSMContext):
    # Validate the full name input
    if is_valid_cyrillic_name(message.text):
        await state.update_data(full_name=message.text)
        await state.set_state(RegistrationState.phone_number)
        await message.answer("📞 Теперь отправьте Ваш номер телефона через +7 следующим сообщением:")
        return
    # If the full name is not valid, prompt the user to enter it again
    await message.answer(Texts.get_name_validation_text(), parse_mode="HTML")


@router.message(RegistrationState.phone_number)
async def get_phone_number(message: Message, state: FSMContext):
    # Validate the phone number input
    if not message.text.startswith("+7") or len(message.text) != 12 or not message.text[2:].isdigit():
        await message.answer(Texts.get_phone_validation_text(), parse_mode="HTML")
        await state.set_state(RegistrationState.phone_number)
        return
    await state.update_data(phone_number=message.text)
    user_data = await state.get_data()
    full_name = user_data.get("full_name")
    phone_number = user_data.get("phone_number")
    user_id = message.from_user.id
    username = message.from_user.username
    # Here you would typically save the user data to the database   
    await add_or_update_user(user_id, username, full_name, phone_number)
    await state.clear()
    await message.answer(Texts.get_main_menu_text(), reply_markup=main_menu_keyboard())

