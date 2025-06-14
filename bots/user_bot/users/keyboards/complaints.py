from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def complaint_navigation_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="complaint_back"),
                InlineKeyboardButton(text="⏭️ Пропустить", callback_data="complaint_skip")
            ]
        ]
    )

def application_choosing_navigation_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📛 Оставить заявку", callback_data="fill_form"), InlineKeyboardButton(text="💡 Поделиться предложением", callback_data="suggestion")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main_menu")]
        ],
        resize_keyboard=True
    )

