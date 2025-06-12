from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def call_application_navigation_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📞 Перезвоните мне", callback_data="contact_call")],
            [InlineKeyboardButton(text="💬 Свяжитесь со мной в чат-боте", callback_data="contact_chat")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="call_application_back")]
        ]
    )

def call_request_navigation_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data="call_confirm"), InlineKeyboardButton(text="✏️ Оставить номер телефона", callback_data="settings_change_phone")]
        ]
    )


def end_chat_navigation_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌📞 Диалог с администратором заканчивается", callback_data="end_chat")]
        ]
    )