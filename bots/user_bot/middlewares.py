from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from bots.common.texts import Texts
from core.config import ADMIN_GROUP_ID
from db.crud.user_crud import get_user_by_telegram_id_or_username
from aiogram.fsm.context import FSMContext
from bots.user_bot.states import RegistrationState
from typing import Callable, Awaitable, Dict

class BlockCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        if isinstance(event, Message):
            user_id = event.from_user.id
            user = await get_user_by_telegram_id_or_username(str(user_id))

            # If user is NOT found — redirect to registration
            if not user:
                state: FSMContext = data['state']
                await state.set_state(RegistrationState.full_name)
                return await handler(event, data)

            # If user is found but blocked — stop interaction
            if user.is_blocked:
                await event.answer("🚫 Вы были заблокированы и не можете пользоваться ботом.")
                return

        return await handler(event, data)
    

ADMINS = {123456789}  # replace with real admin Telegram IDs

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message, data: Dict):
        if event.chat.id != ADMIN_GROUP_ID:
            await event.answer("У вас нет доступа к админ-панели.")
            return
        return await handler(event, data)


