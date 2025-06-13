from bots.common.texts import Texts
from aiogram import Router, F
from aiogram.types import Message

from bots.user_bot.users.keyboards.main_menu import main_menu_keyboard


router = Router()


@router.message(F.text.lower().contains("полезные контакт"))
async def handle_usefull_contacts(message: Message):
    await message.answer(Texts.get_usefull_contacts(), reply_markup=main_menu_keyboard(), parse_mode="HTML")
