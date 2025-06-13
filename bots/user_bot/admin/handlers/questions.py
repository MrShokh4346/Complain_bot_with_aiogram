from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bots.user_bot.admin.keyboards.questions_keyboards import answer_question_navigation_buttons
from bots.user_bot.states import AnswerToQuestionState
from core.config import ADMIN_GROUP_ID
from db.crud.questions_crud import get_all_questions, save_answer_to_question

router = Router()


@router.message(F.text.lower().contains("/questions"))
async def list_questions(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2 or not parts[1].isdigit():
        quantity = 10  # Default quantity if not specified
    else:
        try:
            quantity = int(parts[1])
        except ValueError:
            await message.answer("❗ Укажите корректное количество вопросов для отображения: <code>/questions [количество]</code>", parse_mode="HTML")
            return
    questions = await get_all_questions(quantity)
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
    await callback.message.answer("✏️ Пожалуйста, введите ваш ответ на вопрос.\n❗ Укажите ID вапроса: <code>/questionid_</code>[question_id] ваш ответ", parse_mode="HTML")


@router.message(AnswerToQuestionState.waiting_for_answer, F.text.lower().contains("/questionid"))
async def answer_question(message: Message, state: FSMContext):

    part = message.text.strip().split()[0]
    if not part.startswith("/questionid"):
        await message.answer("❗ Укажите ID вопроса: <code>/questionid_</code>[question_id] ваш ответ", parse_mode="HTML")
        return
    
    parts = part.split("_")
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("❗ Укажите корректный ID вопроса: <code>/questionid_</code>[question_id] ваш ответ", parse_mode="HTML")
        return
    
    entered_question_id = int(parts[1])
    
    data = await state.get_data()
    state_question_id = data.get("question_id")
    if state_question_id != entered_question_id:
        return
    
    answer_text = message.text[len(part):].strip()
    
    question = await save_answer_to_question(state_question_id, answer_text)
    
    await message.answer("Ваш ответ успешно отправлен!")
    
    # Optionally, you can notify the user who asked the question
    await message.bot.send_message(
        question.user_id,
        f"❓ <b>Ваш вопрос:</b>\n{question.question_text}\n\n✅ <b>Ответ администратора:</b>\n{answer_text}",
        parse_mode="HTML"
    )
    await state.clear()


