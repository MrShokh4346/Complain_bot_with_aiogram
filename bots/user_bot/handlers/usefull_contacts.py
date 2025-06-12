from bots.common.texts import Texts
from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove


router = Router()


@router.message(F.text.lower().contains("полезные контакт"))
async def handle_usefull_contacts(message: Message):
    await message.answer(Texts.get_usefull_contacts(), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
