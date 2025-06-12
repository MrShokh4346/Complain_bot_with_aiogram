from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bots.common.texts import Texts
from bots.user_bot.users.keyboards.complaints import application_choosing_navigation_buttons, complaint_navigation_buttons
from bots.user_bot.users.keyboards.main_menu import main_menu_keyboard
from bots.user_bot.states import ComplaintState
from core.config import COMPLAINT_GROUP_ID


router = Router()


@router.callback_query(F.data == "fill_form")
async def start_complaint(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ComplaintState.address)
    await callback.message.edit_text(Texts.get_complaint_address_text(), reply_markup=complaint_navigation_buttons(), parse_mode="HTML")


@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(Texts.get_main_menu_text(), reply_markup=main_menu_keyboard())


@router.message(F.text == "📛 Оставить заявку")
async def show_request_submenu(message: Message, state: FSMContext):
    await message.answer(Texts.get_application_choosing_text(), reply_markup=application_choosing_navigation_buttons())

