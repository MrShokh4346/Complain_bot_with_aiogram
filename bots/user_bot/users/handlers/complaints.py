from aiogram.filters import StateFilter
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bots.common.texts import Texts
from bots.user_bot.users.keyboards.complaints import application_choosing_navigation_buttons, complaint_navigation_buttons, end_complaint_navigation_buttons
from bots.user_bot.users.keyboards.main_menu import main_menu_keyboard
from bots.user_bot.states import  ComplaintState
from core.config import COMPLAINT_GROUP_ID
from core.utils import make_complaint_text
from db.crud.user_crud import get_user_by_id


router = Router()


@router.callback_query(ComplaintState.address, F.data == "complaint_skip")
async def handle_complaint_address_skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(address = "", address_skipped=True)
    await state.set_state(ComplaintState.media)
    await callback.message.edit_text(Texts.get_complaint_media_text(), reply_markup=complaint_navigation_buttons(), parse_mode="HTML")


@router.callback_query(ComplaintState.address, F.data == "complaint_back")
async def handle_complaint_address_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(Texts.get_application_choosing_text(), reply_markup=application_choosing_navigation_buttons())



@router.callback_query(ComplaintState.media, F.data == "complaint_skip")
async def handle_complaint_media_skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(media = None, media_skipped=True)
    await state.set_state(ComplaintState.body)
    await callback.message.edit_text(Texts.get_complaint_body_text(), reply_markup=end_complaint_navigation_buttons(), parse_mode="HTML")


@router.callback_query(ComplaintState.media, F.data == "complaint_back")
async def handle_complaint_media_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await state.set_state(ComplaintState.address)
    await callback.message.edit_text(Texts.get_complaint_address_text(), reply_markup=complaint_navigation_buttons(), parse_mode="HTML")


@router.callback_query(ComplaintState.body, F.data == "complaint_skip")
async def handle_complaint_body_skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_id = callback.from_user.id
    user = await get_user_by_id(user_id)
    if not user:
        await callback.message.answer("Пользователь не найден. Пожалуйста, попробуйте позже.")
        return
    
    data = await state.update_data(body="", body_skipped=True)
    skips = data.get('address_skipped', 0) + data.get('media_skipped', 0) + data.get('body_skipped', 0)
    if skips == 3:
        await callback.message.answer("Вы пропустили все поля. Пожалуйста, заполните хотя бы одно из них.", reply_markup=application_choosing_navigation_buttons(), parse_mode="HTML")
        await state.clear()
        return
    data['user'] = user
    complaint_text = make_complaint_text(data)

    if data.get('media'):
        if data.get('media_type') == "video":
            await callback.message.bot.send_video(COMPLAINT_GROUP_ID, video=data['media'], caption=complaint_text, parse_mode="HTML")
        else:  # default to photo
            await callback.message.bot.send_photo(chat_id=COMPLAINT_GROUP_ID, photo=data['media'], caption=complaint_text, parse_mode="HTML")
    else:
        await callback.message.bot.send_message(COMPLAINT_GROUP_ID, complaint_text, parse_mode="HTML")

    await callback.message.answer(Texts.get_complaint_sent_text(), reply_markup=main_menu_keyboard(), parse_mode="HTML")
    await state.clear()


@router.callback_query(ComplaintState.body, F.data == "complaint_back")
async def handle_complaint_body_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ComplaintState.media)
    await callback.message.edit_text(Texts.get_complaint_media_text(), reply_markup=complaint_navigation_buttons(), parse_mode="HTML")


@router.message(ComplaintState.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(ComplaintState.media)
    await message.answer(Texts.get_complaint_media_text(), reply_markup=complaint_navigation_buttons(), parse_mode="HTML")


@router.message(ComplaintState.media, F.photo | F.video)
async def get_media(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(media=message.photo[-1].file_id if message.photo else (message.video.file_id if message.video else None))
    await state.update_data(media_type="photo" if message.photo else ("video" if message.video else None))
    await state.set_state(ComplaintState.body)
    await message.answer(Texts.get_complaint_body_text(), reply_markup=end_complaint_navigation_buttons(), parse_mode="HTML")


@router.message(StateFilter(ComplaintState.media))
async def handle_invalid_input(message: Message):
    await message.answer(Texts.get_media_validation_text(), parse_mode="HTML")


@router.message(ComplaintState.body)
async def get_body(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user_by_id(user_id)
    if not user:
        await message.answer("Пользователь не найден. Пожалуйста, попробуйте позже.")
        return
    data = await state.update_data(body=message.text)
    data['user'] = user
    complaint_text = make_complaint_text(data)

    if data.get('media'):
        if data.get('media_type') == "video":
            await message.bot.send_video(COMPLAINT_GROUP_ID, video=data['media'], caption=complaint_text, parse_mode="HTML")
        else:  # default to photo
            await message.bot.send_photo(chat_id=COMPLAINT_GROUP_ID, photo=data['media'], caption=complaint_text, parse_mode="HTML")
    else:
        await message.bot.send_message(COMPLAINT_GROUP_ID, complaint_text, parse_mode="HTML")

    await message.answer(Texts.get_complaint_sent_text(), reply_markup=main_menu_keyboard(), parse_mode="Markdown")
    await state.clear()

