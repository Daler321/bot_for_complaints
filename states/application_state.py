from aiogram.fsm.state import State, StatesGroup

class ApplicationState(StatesGroup):
  leave_application = State()
  offer = State()
  first_step = State()
  seccond_step = State()
  theerd_step = State()
  address = State()
  photo = State()
  video = State()