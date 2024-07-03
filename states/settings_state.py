from aiogram.fsm.state import State, StatesGroup

class SettingsForm(StatesGroup):
  name = State()
  number = State()