from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from states.settings_state import SettingsForm
from keyboards.main_keyboard import main_keyboard

from utils.user_validation import isValidName, isValidNumber
from database.user_db import update_user_name, update_user_number

from config import texts as answers

settings_answers = answers["settings_route_messages"]
bad_answers = answers["bad_answers"]

router = Router()

@router.callback_query(F.data == 'change_name')
async def change_name_handler(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await state.set_state(SettingsForm.name)
  await callback.message.answer(settings_answers["change_name"])

@router.message(SettingsForm.name)
async def handel_name(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  new_name = message.text
  if not isValidName(new_name):
    return await message.answer(bad_answers["no_valid_name"])
  await update_user_name(user_id, new_name)
  await state.clear()
  return await message.answer(settings_answers["change_name_success"], reply_markup=main_keyboard)

@router.callback_query(F.data == 'change_number')
async def change_number_handler(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await state.set_state(SettingsForm.number)
  await callback.message.answer(settings_answers["change_number"])

@router.message(SettingsForm.number)
async def handel_number(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  new_number = message.text
  if not isValidNumber(new_number):
    return await message.answer(bad_answers["no_valid_number"])
  await update_user_number(user_id, new_number)
  await state.clear()
  return await message.answer(settings_answers["change_number_success"], reply_markup=main_keyboard)

