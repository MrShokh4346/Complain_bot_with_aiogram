from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bots.user_bot.admin.keyboards.questions_keyboards import answer_question_navigation_buttons
from bots.user_bot.states import AnswerToQuestionState
from core.config import ADMIN_GROUP_ID
from db.crud.questions_crud import get_all_questions, save_answer_to_question

router = Router()


@router.message(F.text == "/questions")
async def list_questions(message: Message):
    questions = await get_all_questions()
    if len(questions) == 0:
        await message.answer("❗ Нет вопросов для ответа.")
        return
    for q in questions:
        await message.answer(
            f"❓ Вопрос от @{q.user.username  or '—'} ({q.user.full_name}):\n<b>Question ID:</b> {q.id}\n{q.question_text}", 
            reply_markup=answer_question_navigation_buttons(q.id), parse_mode="HTML")


@router.callback_query(F.data.lower().contains("answer_"))
async def confirm_call(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AnswerToQuestionState.waiting_for_answer)
    await state.update_data(question_id=int(callback.data.split("_")[1]))
    await callback.message.answer("✏️ Пожалуйста, введите ваш ответ на вопрос.\n❗ Укажите ID вапроса: `/questionid_<question_id> ...`")


@router.message(AnswerToQuestionState.waiting_for_answer, F.text.lower().contains("/questionid"))
async def answer_question(message: Message, state: FSMContext):

    part = message.text.strip().split()[0]
    if not part.startswith("/questionid"):
        await message.answer("❗ Укажите ID вопроса: `/questionid_<question_id> ...`")
        return
    
    parts = part.split("_")
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("❗ Укажите корректный ID вопроса: `/questionid_<question_id> ...`")
        return
    
    entered_question_id = int(parts[1])
    
    data = await state.get_data()
    state_question_id = data.get("question_id")
    if state_question_id != entered_question_id:
        return
    
    question = await save_answer_to_question(state_question_id, message.text)
    
    await message.answer("Ваш ответ успешно отправлен!")
    
    # Optionally, you can notify the user who asked the question
    await message.bot.send_message(
        question.user_id,
        f"Ваш вопрос:\n{question.question_text}\n\nОтвет администратора:\n{message.text}"
    )
    await state.clear()


