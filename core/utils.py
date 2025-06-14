from db.crud.user_crud import get_user_by_telegram_id_or_username
from db.models import Question, User
from sqlalchemy import select, or_
from db.base import async_session_maker
import re

def is_valid_cyrillic_name(full_name: str) -> bool:
    pattern = r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$"
    return bool(re.match(pattern, full_name))


async def make_user_info_text(parts: list) -> str:
    
    user_id = parts[1]
    user = await get_user_by_telegram_id_or_username(user_id)
    if user:
        info = (
            f"👤 ID: {user.id}\n"
            f"🔸 Username: @{user.username}\n"
            f"👤 Имя и Фамилия: {user.full_name}\n"
            f"📞 Телефон: {user.phone_number}\n"
            f"📅 Зарегистрирован: {user.created_at.strftime("%Y-%m-%d %H:%M")}\n"
            f"🚫 Заблокирован: {'Да' if user.is_blocked else 'Нет'}"
        )
        return info
    info = ("❗ Пользователь не найден. ")
    return info


def make_complaint_text(data: dict) -> str:
    user = data.get("user")
    return (
            f"<b>⛔️ Поступила новая жалоба:</b>\n"
            f"@{user.username or '—'} (id: {user.id})\n"
            f"<b>Имя и Фамилия:</b> {user.full_name or '—'}\n"
            f"<b>Номер телефона:</b> {user.phone_number}\n"
            f"<b>Адрес:</b> {data['address']}\n"
            f"<b>Содержание:</b> {data['body']}\n"
            # f"🆔 reply_to_user_id:{user.id}"
        )


def make_suggestion_text(data: dict) -> str:
    user = data.get("user")
    return (
            f"<b>⛔️ Поступила новая предложение :</b>\n"
            f"@{user.username or '—'} (id: {user.id})\n"
            f"<b>Имя и Фамилия:</b> {user.full_name or '—'}\n"
            f"<b>Номер телефона:</b> {user.phone_number}\n"
            f"<b>Содержание:</b> {data['body']}\n"
            # f"🆔 reply_to_user_id:{user.id}"
        )


def make_callback_application(data: dict) -> str:
    user = data.get("user")
    return (
            f"<b>📞 Пользователь просит перезвонить:</b>\n"
            f"@{user.username or '—'}\n"
            f"<b>Имя и Фамилия:</b> {user.full_name or '—'}\n"
            f"<b>Номер телефона:</b> {user.phone_number}\n"
            # f"🆔 reply_to_user_id:{user.id}"
        )
