from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bots.admin_bot.states import BroadcastState
from db.crud import get_all_user_ids

router = Router()

@router.callback_query(F.data == "admin_broadcast")
async def ask_broadcast_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите сообщение для рассылки (можно с фото/видео):")
    await state.set_state(BroadcastState.waiting_for_content)
    await callback.answer()

@router.message(BroadcastState.waiting_for_content)
async def send_broadcast(message: Message, state: FSMContext):
    user_ids = await get_all_user_ids()
    success = failed = 0

    for user_id in user_ids:
        try:
            if message.photo:
                await message.bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption or "")
            elif message.video:
                await message.bot.send_video(user_id, video=message.video.file_id, caption=message.caption or "")
            else:
                await message.bot.send_message(user_id, message.text)
            success += 1
        except:
            failed += 1

    await message.answer(f"Рассылка завершена.\n✅ Отправлено: {success}\n❌ Ошибка: {failed}")
    await state.clear()
