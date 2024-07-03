from aiogram.fsm.state import State, StatesGroup

class AppState(StatesGroup):
  route_chain = State()
  main = State()
  leave_request = State()
  constact = State()
  settings = State()
  helpful_contacts = State()
