import datetime
from db.base import async_session_maker
from sqlalchemy import or_, select
from db.models import Question, User
from sqlalchemy.orm import selectinload
from db.base import async_session_maker

async def get_questions_by_user_id(user_id: int):
    async with async_session_maker() as session:
        questions = await session.execute(select(Question).where(Question.is_answered == False, Question.user_id == user_id))
        return questions.scalars().all()
    

async def get_all_questions():
    async with async_session_maker() as session:
        questions = await session.execute(select(Question).options(selectinload(Question.user)).where(Question.is_answered == False))
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
    

