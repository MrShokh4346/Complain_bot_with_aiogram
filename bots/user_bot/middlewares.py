from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from db.crud import get_user_by_telegram_id_or_username
from aiogram.fsm.context import FSMContext
from bots.user_bot.states import RegistrationState

class BlockCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        if isinstance(event, Message):
            user_id = event.from_user.id
            user = await get_user_by_telegram_id_or_username(str(user_id))

            # If user is NOT found — redirect to registration
            if not user:
                state: FSMContext = data['state']
                await state.set_state(RegistrationState.full_name)
                await event.answer("👋 Доброго времени суток, бот создан, чтобы обрабатывать заявки и обращения пользователей. Чтобы воспользоваться этим, пришлите для начала Ваше Имя и Фамилию")
                return  # Stop further processing

            # If user is found but blocked — stop interaction
            if user.is_blocked:
                await event.answer("🚫 Вы были заблокированы и не можете пользоваться ботом.")
                return

        return await handler(event, data)
