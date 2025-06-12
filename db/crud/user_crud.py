import datetime
from db.base import async_session_maker
from sqlalchemy import or_, select
from db.models import User
from db.base import async_session_maker

async def get_user_by_id(user_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

async def add_or_update_user(user_id: int, username: str = None, full_name: str = None, phone_number: str = None):
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            user = User(id=user_id, username=username, full_name=full_name, phone_number=phone_number)
            session.add(user)
        else:
            if full_name:
                user.full_name = full_name
            if phone_number:
                user.phone_number = phone_number
            user.updated_at = datetime.datetime.now()
        await session.commit()
        return user

async def get_all_active_users():
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.is_blocked == False))
        return result.scalars().all()
    

async def get_all_users():
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        return result.scalars().all()
    

# async def block_user(user_id: int):
#     async with async_session_maker() as session:
#         user = await get_user_by_id(user_id)
#         if user:
#             user.is_blocked = True
#             await session.commit()
#             return True
#         return False

# async def unblock_user(user_id: int):
#     async with async_session_maker() as session:
#         user = await get_user_by_id(user_id)
#         if user:
#             user.is_blocked = False
#             await session.commit()
#             return True
#         return False

# async def add_complaint(user_id: int, message_id: int, chat_id: int):
#     async with async_session_maker() as session:
#         complaint = Complaint(user_id=user_id, message_id=message_id, chat_id=chat_id)
#         session.add(complaint)
#         await session.commit()
#         return complaint

# async def get_latest_complaint(user_id: int):
#     async with async_session_maker() as session:
#         result = await session.execute(
#             select(Complaint)
#             .where(Complaint.user_id == user_id)
#             .order_by(Complaint.created_at.desc())
#             .limit(1)
#         )
#         return result.scalars().first()


async def set_user_block_status(query: str, block: bool) -> bool:
    async with async_session_maker() as session:
        stmt = select(User).where(
            or_(
                User.id == int(query) if query.isdigit() else False,
                User.username == query
            )
        )
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            return False
        user.is_blocked = block
        await session.commit()
        return True
    
    
async def get_user_by_telegram_id_or_username(query: str):
    async with async_session_maker() as session:
        stmt = select(User).where(
            or_(
                User.id == int(query) if query.isdigit() else False,
                User.username == query
            )
        )
        result = await session.execute(stmt)
        return result.scalars().first()


