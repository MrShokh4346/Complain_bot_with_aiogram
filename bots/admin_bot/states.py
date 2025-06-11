from aiogram.fsm.state import StatesGroup, State

class BroadcastState(StatesGroup):
    waiting_for_content = State()
