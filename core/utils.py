from db.models import User
from sqlalchemy import select, or_
from db.base import async_session_maker
import re

def is_valid_cyrillic_name(full_name: str) -> bool:
    pattern = r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$"
    return bool(re.match(pattern, full_name))


def make_complaint_text(data: dict) -> str:
    user = data.get("user")
    return (
            f"<b>⛔️ Поступила новая жалоба:</b>\n"
            f"@{user.username or '—'}\n"
            f"<b>Имя и Фамилия:</b> {user.full_name or '—'}\n"
            f"<b>Номер телефона:</b> {user.phone_number}\n"
            f"<b>Адрес:</b> {data['address']}\n"
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


async def get_all_user_ids():
    async with async_session_maker() as session:
        result = await session.execute(select(User.telegram_id))
        return [row[0] for row in result.all()]


async def get_user_by_telegram_id_or_username(query: str):
    async with async_session_maker() as session:
        stmt = select(User).where(
            or_(
                User.telegram_id == int(query) if query.isdigit() else False,
                User.username == query
            )
        )
        result = await session.execute(stmt)
        return result.scalars().first()
    

