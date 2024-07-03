from aiogram.fsm.state import State, StatesGroup

class RegForm(StatesGroup):
  admin_register = State()
  name = State()
  number = State()