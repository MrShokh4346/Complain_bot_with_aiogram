from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def settings_navigation_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛠 Поменять имя", callback_data="settings_change_name"),
                InlineKeyboardButton(text="🛠 Сменить номер", callback_data="settings_change_phone")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="settings_back")
            ]
        ]
    )