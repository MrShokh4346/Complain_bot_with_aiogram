from bots.user_bot.states import SuggestionState
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bots.user_bot.states import ComplaintState
from core.config import COMPLAINT_GROUP_ID
import os

router = Router()


@router.callback_query(F.data == "suggest_solution")
async def handle_suggestion_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Пожалуйста, напишите ваше предложение:")



@router.message(F.text.lower().contains("предложен"))
async def start_suggestion(message: Message, state: FSMContext):
    await state.set_state(SuggestionState.media)
    await message.answer("Вы можете прикрепить фото или видео к своему предложению. Если у Вас нет медиа — напишите 'Пропустить'.")

@router.message(SuggestionState.media, F.photo | F.video | F.text.lower() == "пропустить")
async def get_suggestion_media(message: Message, state: FSMContext):
    media_id = message.photo[-1].file_id if message.photo else (message.video.file_id if message.video else None)
    await state.update_data(media=media_id)
    await state.set_state(SuggestionState.body)
    await message.answer("Пожалуйста, введите текст Вашего предложения:")

@router.message(SuggestionState.body)
async def get_suggestion_body(message: Message, state: FSMContext):
    user = message.from_user
    data = await state.update_data(body=message.text)

    suggestion_text = (
        f"<b>Новое предложение</b>\n"
        f"👤 Пользователь: @{user.username or '—'} (id: <code>{user.id}</code>)\n"
        f"✉️ Идея: {data['body']}"
    )

    if data.get("media"):
        await message.bot.send_photo(COMPLAINT_GROUP_ID, photo=data["media"], caption=suggestion_text)
    else:
        await message.bot.send_message(COMPLAINT_GROUP_ID, suggestion_text)

    await message.answer("Спасибо! Ваше предложение отправлено.", reply_markup=ReplyKeyboardRemove())
    await state.clear()