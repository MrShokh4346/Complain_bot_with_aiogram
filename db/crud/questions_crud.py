import datetime
from db.base import async_session_maker
from sqlalchemy import  desc, select
from db.models import Question, User
from sqlalchemy.orm import selectinload
from db.base import async_session_maker

async def get_questions_by_user_id(user_id: int):
    async with async_session_maker() as session:
        questions = await session.execute(select(Question).where(Question.is_answered == False, Question.user_id == user_id))
        return questions.scalars().all()
    

async def get_all_questions(quantity: int = 10):
    async with async_session_maker() as session:
        questions = await session.execute(select(Question).options(selectinload(Question.user)).where(Question.is_answered == False).order_by(desc(Question.id)) .limit(quantity))
        return questions.scalars().all()
    

async def save_answer_to_question(question_id: int, answer_text: str):
    async with async_session_maker() as session:
        question = await session.get(Question, question_id)
        if question:
            question.answer_text = answer_text
            question.is_answered = True
            question.answered_at = datetime.datetime.now()
            await session.commit()
            return question
        return ""
    

async def save_question(text: str, user_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return None
        question = Question(user_id=user.id, question_text = text, user=user)
        session.add(question)
        await session.commit()
        return f"💬 Новое сообщение от @{user.username or '—'} ({user.full_name}):\n<b>Question ID:</b> {question.id} \n{text}", question.id
    