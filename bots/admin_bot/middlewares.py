from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict

ADMINS = {123456789}  # replace with real admin Telegram IDs

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message, data: Dict):
        if event.from_user.id not in ADMINS:
            await event.answer("У вас нет доступа к админ-панели.")
            return
        return await handler(event, data)

