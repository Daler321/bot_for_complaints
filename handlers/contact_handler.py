from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter

from keyboards.main_keyboard import main_keyboard
from keyboards.contact_keyboard import is_right_number_keyboard, chat_keyboard

from utils.user_validation import isValidNumber
from database.user_db import take_user
from database.admin_db import take_aproved_admins
from states.contact_state import ContactState

from config import texts as answers

contact_answers = answers["contact_route_messages"]
bad_answers = answers["bad_answers"]

router = Router()

class FeedBackFilter(Filter):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, message: types.Message) -> bool:
        return bool(message.reply_to_message) and '#' in message.reply_to_message.text

@router.message(FeedBackFilter())
async def test_filter(message: types.Message):
  from bot import send_message
  id = message.reply_to_message.text.split('#')[-1]
  await send_message(chat_id=id, text=message.text, reply_markup=chat_keyboard)

@router.callback_query(F.data == 'call')
async def call_handler(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()
  user = await take_user(callback.from_user.id)
  phone_number = user.number
  await callback.message.answer(contact_answers["call"].replace('phone_number', phone_number), reply_markup=is_right_number_keyboard)

@router.callback_query(F.data == 'chat')
async def chat_handler(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await state.set_state(ContactState.chat)
  await callback.message.answer(contact_answers["chat"], reply_markup=chat_keyboard)

@router.callback_query(F.data == 'end_chat')
async def chat_handler(callback: types.CallbackQuery, state: FSMContext):
  await state.clear()
  from bot import send_message
  user = await take_user(callback.from_user.id)
  admins = await take_aproved_admins()
  for x in admins:
    await send_message(x.id, f'User {user.name} with ID #{str(user.id)} end chat')
  await callback.message.answer(contact_answers["chat_end"], reply_markup=main_keyboard)
  
@router.message(ContactState.chat)
async def chat_handler(message: types.Message, state: FSMContext):
  from bot import send_message
  text = message.text
  user = await take_user(message.from_user.id)
  admins = await take_aproved_admins()
  for x in admins:
    await send_message(x.id, f'User {user.name} with ID #{str(user.id)} message:\n{text}')

@router.callback_query(F.data == 'yes')
async def call_req_handler(callback: types.CallbackQuery, state: FSMContext):
  from bot import send_message
  # take admin group
  user = await take_user(callback.from_user.id)
  admins = await take_aproved_admins()
  for x in admins:
    await send_message(x.id, f'User {user.name} with ID {str(user.id)} ask to call on number: {user.number}')
  # send message to admins group  
  await callback.message.answer(contact_answers["call_req"], reply_markup=main_keyboard)

@router.callback_query(F.data == 'leave_number')
async def leave_number_handler(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await state.set_state(ContactState.leave_number)
  await callback.message.answer("Please leave number for conct")

@router.message(ContactState.leave_number)
async def handel_number(message: types.Message, state: FSMContext):
  from bot import send_message
  new_number = message.text
  if not isValidNumber(new_number):
    return await message.answer(bad_answers["no_valid_number"])
  user = await take_user(message.from_user.id)
  admins = await take_aproved_admins()
  for x in admins:
    await send_message(x.id, f'User {user.name} with ID {str(user.id)} ask to call on number: {new_number}')
  await state.clear()
  await message.answer(contact_answers["call_req"], reply_markup=main_keyboard)
