from aiogram.fsm.state import State, StatesGroup

class RegistrationState(StatesGroup):
    full_name = State()
    phone_number = State()
    registering = State()  # State to handle the registration process


class ComplaintState(StatesGroup):
    address = State()
    media = State()
    media_type = State()  # State to handle media type selection
    body = State()
    address_skipped= State()  # State to handle skips in the complaint process
    media_skipped= State()  # State to handle skips in the complaint process
    body_skipped= State()  # State to handle skips in the complaint process
    

class SuggestionState(StatesGroup):
    media = State()
    media_type = State()  # State to handle media type selection
    body = State()
    media_skipped= State()  # State to handle skips in the complaint process
    body_skipped= State()


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
