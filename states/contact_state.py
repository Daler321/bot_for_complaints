from aiogram.fsm.state import State, StatesGroup

class ContactState(StatesGroup):
  leave_number = State()
  chat = State()