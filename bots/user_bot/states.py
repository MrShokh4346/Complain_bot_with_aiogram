from aiogram.fsm.state import State, StatesGroup

class RegistrationState(StatesGroup):
    full_name = State()
    phone_number = State()


class ComplaintState(StatesGroup):
    address = State()
    media = State()
    body = State()
    address_skipped= State()  # State to handle skips in the complaint process
    media_skipped= State()  # State to handle skips in the complaint process
    body_skipped= State()  # State to handle skips in the complaint process

class SuggestionState(StatesGroup):
    media = State()
    body = State()

class ContactCallState(StatesGroup):
    confirm = State()
    wait_phone = State()

class ChatSupportState(StatesGroup):
    chat = State()

class SettingsState(StatesGroup):
    set_name = State()
    set_phone = State()

class BroadcastState(StatesGroup):
    waiting_for_content = State()


class AnswerToQuestionState(StatesGroup):
    waiting_for_answer = State()
    question_id = State()  # To store the ID of the question being answered
