from aiogram.filters import StateFilter
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bots.common.texts import Texts
from bots.user_bot.users.keyboards.complaints import application_choosing_navigation_buttons, complaint_navigation_buttons
from bots.user_bot.users.keyboards.main_menu import main_menu_keyboard
from bots.user_bot.states import  SuggestionState
from bots.user_bot.users.keyboards.suggestion import suggestion_navigation_buttons
from core.config import COMPLAINT_GROUP_ID
from core.utils import make_complaint_text, make_suggestion_text
from db.crud.user_crud import get_user_by_id


router = Router()


@router.callback_query(SuggestionState.media, F.data == "suggestion_skip")
async def handle_suggestion_media_skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(media = None, media_skipped=True)
    await state.set_state(SuggestionState.body)
    await callback.message.edit_text(Texts.get_suggestion_body_text(), reply_markup=suggestion_navigation_buttons(), parse_mode="HTML")


@router.callback_query(SuggestionState.media, F.data == "suggestion_back")
async def handle_suggestion_media_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SuggestionState.media)
    await callback.message.edit_text(Texts.get_application_choosing_text(), reply_markup=application_choosing_navigation_buttons(), parse_mode="HTML")


@router.callback_query(SuggestionState.body, F.data == "suggestion_skip")
async def handle_suggestion_body_skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    user = await get_user_by_id(user_id)
    if not user:
        await callback.message.answer("Пользователь не найден. Пожалуйста, попробуйте позже.")
        return
    
    data = await state.update_data(body="", body_skipped=True)
    skips = data.get('media_skipped', 0) + data.get('body_skipped', 0)
    if skips == 2:
        await callback.message.answer("Вы пропустили все поля. Пожалуйста, заполните хотя бы одно из них.", reply_markup=application_choosing_navigation_buttons(), parse_mode="HTML")
        await state.clear()
        return
    data['user'] = user
    complaint_text = make_suggestion_text(data)

    if data.get('media'):
        if data.get('media_type') == "video":
            await callback.message.bot.send_video(COMPLAINT_GROUP_ID, video=data['media'], caption=complaint_text, parse_mode="HTML")
        else:  # default to photo
            await callback.message.bot.send_photo(chat_id=COMPLAINT_GROUP_ID, photo=data['media'], caption=complaint_text, parse_mode="HTML")
    else:
        await callback.message.bot.send_message(COMPLAINT_GROUP_ID, complaint_text, parse_mode="HTML")

    await callback.message.answer(Texts.get_suggestion_sent_text(), reply_markup=main_menu_keyboard(), parse_mode="HTML")
    await state.clear()


@router.callback_query(SuggestionState.body, F.data == "suggestion_back")
async def handle_suggestion_body_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SuggestionState.media)
    await callback.message.edit_text(Texts.get_suggestion_media_text(), reply_markup=suggestion_navigation_buttons(), parse_mode="HTML")


@router.message(SuggestionState.media, F.photo | F.video)
async def get_suggestion_media(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(media=message.photo[-1].file_id if message.photo else (message.video.file_id if message.video else None))
    await state.update_data(media_type="photo" if message.photo else ("video" if message.video else None))
    await state.set_state(SuggestionState.body)
    await message.answer(Texts.get_suggestion_body_text(), reply_markup=suggestion_navigation_buttons(), parse_mode="HTML")


@router.message(StateFilter(SuggestionState.media))
async def handle_suggestion_invalid_input(message: Message):
    await message.answer("❌ Пожалуйста, отправьте фото или видео. Другие типы сообщений не принимаются на этом этапе.")


@router.message(SuggestionState.body)
async def get_suggestion_body(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user_by_id(user_id)
    if not user:
        await message.answer("Пользователь не найден. Пожалуйста, попробуйте позже.")
        return
    data = await state.update_data(body=message.text)
    data['user'] = user
    complaint_text = make_suggestion_text(data)

    if data.get('media'):
        if data.get('media_type') == "video":
            await message.bot.send_video(COMPLAINT_GROUP_ID, video=data['media'], caption=complaint_text, parse_mode="HTML")
        else:  # default to photo
            await message.bot.send_photo(chat_id=COMPLAINT_GROUP_ID, photo=data['media'], caption=complaint_text, parse_mode="HTML")
    else:
        await message.bot.send_message(COMPLAINT_GROUP_ID, complaint_text, parse_mode="HTML")

    await message.answer(Texts.get_suggestion_sent_text(), reply_markup=main_menu_keyboard(), parse_mode="HTML")
    await state.clear()