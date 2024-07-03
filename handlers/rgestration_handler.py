from aiogram import Router, types
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from states.user_reg_states import RegForm
from keyboards.main_keyboard import main_keyboard

from database.user_db import is_user_exists, create_user
from database.admin_db import try_approve, create_admin, is_admin_exists, is_admin_approved, is_admin_banned
from utils.user_validation import isValidName, isValidNumber
from config import texts as answers

bad_answers = answers["bad_answers"]
register_answers = answers["register_answers"]

router = Router()

@router.message(Command('admin'))
async def admin_handler(message: types.Message, state: FSMContext):
  chat_id = message.chat.id
  # is admin group exists
  if await is_admin_exists(chat_id):
    if await is_admin_banned(chat_id):
      await message.answer("You cant be admin")
    elif await is_admin_approved(chat_id):
      await message.answer("You already is admin")
    else:
      await state.set_state(RegForm.admin_register)
      await message.answer("try to enter password")
  else: 
    await create_admin(chat_id)
    await state.set_state(RegForm.admin_register)
    await message.answer("If you want add this bot to admin group please enter the password, you have only 3 attampts, if password not right 3 times you will be blocked")

@router.message(RegForm.admin_register)
async def admin_register_handler(message: types.Message, state: FSMContext):
  chat_id = message.chat.id
  password = message.text
  answer = await try_approve(chat_id, password)
  if answer == 'Approved' or answer == 'Banned':
    await state.clear()
  return await message.answer(answer)

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
  if await is_user_exists(message.from_user.id):
    return await message.answer(answers["main_routes_messages"]["main"],
                       reply_markup=main_keyboard)
  await state.set_state(RegForm.name)
  await message.answer(register_answers["name_req_message"])

@router.message(RegForm.name)
async def handel_name(message: types.Message, state: FSMContext):
  name = message.text
  if not isValidName(name):
    return await message.answer(bad_answers["no_valid_name"])
  await state.update_data(name=name)
  await state.set_state(RegForm.number)
  await message.answer(register_answers["number_req_message"])

@router.message(RegForm.number)
async def handel_number(message: types.Message, state: FSMContext):
  number = message.text
  if not isValidNumber(number):
    return await message.answer(bad_answers["no_valid_number"])
  await state.update_data(number=number)
  await message.answer(answers["main_routes_messages"]["main"],
                       reply_markup=main_keyboard)
  user_state = await state.get_data()
  await create_user(message.from_user.id, user_state.get('name'), user_state.get('number'))
  await state.clear()
