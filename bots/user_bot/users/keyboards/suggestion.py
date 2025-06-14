from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def suggestion_navigation_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="suggestion_back"),
                InlineKeyboardButton(text="⏭️ Пропустить", callback_data="suggestion_skip")
            ]
        ]
    )