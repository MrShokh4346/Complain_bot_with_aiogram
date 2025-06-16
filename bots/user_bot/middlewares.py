from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, ReplyKeyboardRemove
from bots.common.texts import Texts
from core.config import ADMIN_GROUP_ID
from db.crud.user_crud import get_user_by_telegram_id_or_username
from aiogram.fsm.context import FSMContext
from bots.user_bot.states import RegistrationState
from typing import Callable, Awaitable, Dict, Any


class BlockCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        if isinstance(event, Message):
            user_id = event.from_user.id
            state: FSMContext = data['state']
            state_data = await state.get_data()

            user = await get_user_by_telegram_id_or_username(str(user_id))
            # If user is found but blocked — stop interaction
            if (not user) and (state_data.get("registering") == True):
                return await handler(event, data)
            if user.is_blocked:
                await event.answer("🚫 Вы были заблокированы и не можете пользоваться ботом.")
                return

        return await handler(event, data)
    

class CheckRegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message, data: Dict):
        if isinstance(event, Message):
            user_id = event.from_user.id
            user = await get_user_by_telegram_id_or_username(str(user_id))
            state: FSMContext = data['state']
            state_data = await state.get_data()
            
            if state_data.get("registering") == True:
                # If user is registering, skip the check
                return await handler(event, data)

            # If user is NOT found — redirect to registration
            if not user:
                await state.clear()
                await state.set_state(RegistrationState.full_name)
                await state.set_data({"registering": True})
                if event.text != "/start":
                    await event.answer("Вы не зарегистрированы в боте.", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
                await event.answer(Texts.get_registration_text())
                return

        return await handler(event, data)
