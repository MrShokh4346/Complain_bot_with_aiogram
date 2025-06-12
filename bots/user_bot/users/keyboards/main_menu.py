from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📛 Оставить заявку"), KeyboardButton(text="📞 Связаться")],
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="📚 Полезные контакты")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие из меню"
    )
