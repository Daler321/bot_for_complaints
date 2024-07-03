from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from keyboards.settings_keyboard import settings_keyboard
from keyboards.contact_keyboard import contact_keyboard
from keyboards.main_keyboard import main_keyboard
from keyboards.application_keyboard import application_keyboard
from states.app_state import AppState

from config import texts as answers

main_answers = answers["main_routes_messages"]
main_keyboard_text = answers["keyboards"]["main_keyboard"]

router = Router()

@router.message(AppState.main)
async def main_handler(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.answer(main_answers["main"], reply_markup=main_keyboard)
  await state.clear()
  await route_chain_initialization(state)

@router.message(F.text == main_keyboard_text["contact"])
async def settings_handler(message: types.Message, state: FSMContext):
  msg = await message.answer('_', reply_markup=types.ReplyKeyboardRemove())
  await msg.delete()
  await message.answer(main_answers["contact"], reply_markup=contact_keyboard)
  await route_chain_initialization(state)
  await push_chain_link(state, settings_handler)

    
@router.message(F.text == main_keyboard_text["helpful_contacts"])
async def helpful_contacts_handler(message: types.Message):
  await message.answer(main_answers["helpful_contacts"])

@router.message(F.text == main_keyboard_text["settings"] )
async def contact_handler(message: types.Message, state: FSMContext):
    msg = await message.answer('_', reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()
    await message.answer(main_answers["settings"], reply_markup=settings_keyboard)
    await route_chain_initialization(state)
    await push_chain_link(state, contact_handler)

@router.message(F.text == main_keyboard_text["leave_application"] )
async def application_handler(message: types.Message, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
      message = message.message
    msg = await message.answer('_', reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()
    await message.answer(main_answers["chose"], reply_markup=application_keyboard)
    await route_chain_initialization(state)
    await push_chain_link(state, application_handler)

# @router.message(F.text == '📞Связаться')
# async def contact_handler(message: types.Message):
#   await message.answer('👇Выберите способ связи из нижеперечисленного списка:', 
#                        reply_markup=contact_keyboard)

async def route_chain_initialization(state: FSMContext):
  await state.update_data(route_chain=[main_handler])

async def push_chain_link(state: FSMContext, new_link):
  current_state = await state.get_data()
  current_chain = current_state.get("route_chain")
  current_chain.append(new_link)
  await state.update_data(route_chain=current_chain)
  
@router.callback_query(F.data == 'back')
async def back(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()
  current_state = await state.get_data()
  current_chain = current_state.get("route_chain")
  current_chain.pop(-1)
  await state.update_data(route_chain=current_chain)
  await current_chain[-1](callback, state)
  # match current_state:
  #   case AppState.settings:
  #     return await main_handler(callback, state)
  #   case _:
  #     return await main_handler(callback, state)