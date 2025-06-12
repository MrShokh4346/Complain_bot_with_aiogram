from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def answer_question_navigation_buttons(q_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ответить", callback_data=f"answer_{q_id}")]
        ]
    )
