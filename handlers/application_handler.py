from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter

from keyboards.main_keyboard import main_keyboard
from keyboards.application_keyboard import back_keyboard, back_skip_keyboard

from handlers.main_handler import push_chain_link
from database.user_db import take_user
from database.admin_db import take_aproved_admins
from states.application_state import ApplicationState

from config import texts as answers

application_answers = answers["leave_application_route_messages"]

router = Router()

@router.callback_query(F.data == 'offer')
async def offer_handler(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await state.set_state(ApplicationState.offer)
  await push_chain_link(state, offer_handler)
  await callback.message.answer(application_answers["offer"], reply_markup=back_keyboard)

@router.message(ApplicationState.offer)
async def leave_offer(message: types.Message, state: FSMContext):
  if not message.text: 
    return await message.answer(application_answers["fail_offer"])
  from bot import send_message
  text = message.text
  user = await take_user(message.from_user.id)
  admins = await take_aproved_admins()
  for x in admins:
    await send_message(x.id, application_answers['offer_to_admin'].replace('username', message.from_user.username).replace('name', user.name).replace('phone_number', user.number).replace('content', text))
  await state.clear()
  await message.answer(application_answers['offer_sended'], reply_markup=main_keyboard)

@router.callback_query(F.data == 'application')
async def application_first_step_start(callback: types.CallbackQuery, state: FSMContext):
  await state.set_state(ApplicationState.first_step)
  await push_chain_link(state, application_first_step)
  await callback.message.answer(application_answers["leave_first_step"], reply_markup=back_skip_keyboard)

async def application_first_step(callback: types.CallbackQuery, state: FSMContext):
  await state.set_state(ApplicationState.first_step)
  await callback.message.answer(application_answers["leave_first_step"], reply_markup=back_skip_keyboard)

async def application_seccond_step(callback: types.CallbackQuery, state: FSMContext):
  await state.set_state(ApplicationState.seccond_step)
  await callback.message.answer(application_answers["leave_seccond_step"], reply_markup=back_skip_keyboard)
  
async def application_theerd_step(callback: types.CallbackQuery, state: FSMContext):
  await state.set_state(ApplicationState.theerd_step)
  await callback.message.answer(application_answers["leave_theerd_step"], reply_markup=back_keyboard)
  
@router.message(ApplicationState.first_step)
async def application_first_step_handler(message: types.Message, state: FSMContext):
  if not message.text:
    return message.answer('you have to enter text')
  text = message.text
  await state.update_data(address=text)
  await push_chain_link(state, application_seccond_step)
  await state.set_state(ApplicationState.seccond_step)
  await message.answer(application_answers["leave_seccond_step"], reply_markup=back_skip_keyboard)


@router.message(ApplicationState.seccond_step)
async def application_seccond_step_handler(message: types.Message, state: FSMContext):
  # if isinstance(message, types.CallbackQuery):
  #   message = message.message
  if message.photo:
    await state.update_data(photo=message.photo[-1].file_id)
  elif message.video:
    await state.update_data(video=message.video.file_id)
  else:
      return message.answer(application_answers["fail_media"], reply_markup=back_skip_keyboard)

  await push_chain_link(state, application_theerd_step)
  await state.set_state(ApplicationState.theerd_step)
  await message.answer(application_answers["leave_theerd_step"], reply_markup=back_keyboard)

@router.message(ApplicationState.theerd_step)
async def application_theerd_step_handler(message: types.Message, state: FSMContext):
  if not message.text:
    return message.answer('you have to enter text')
  from bot import send_message, bot
  text = message.text
  media_state = await state.get_data()
  address = media_state.get('address', '')
  photo = media_state.get('photo')
  video = media_state.get('video')
  user = await take_user(message.from_user.id)
  admins = await take_aproved_admins()
  for x in admins:
    if photo:
      await bot.send_photo(x.id, photo) 
    if video:
      await bot.send_video(x.id, video) 
    await send_message(x.id, application_answers['application_to_admin'].replace('username', message.from_user.username).replace('name', user.name).replace('phone_number', user.number).replace('content', text).replace('address', address))
  await state.clear()
  await message.answer(application_answers["leave_success"], reply_markup=main_keyboard)

@router.callback_query(F.data == 'skip')
async def skip_handler(callback: types.CallbackQuery, state: FSMContext):
  current_state = await state.get_state()
  if current_state == ApplicationState.first_step:
    await push_chain_link(state, application_seccond_step)
    await state.set_state(ApplicationState.seccond_step)
    return await callback.message.answer(application_answers["leave_seccond_step"], reply_markup=back_skip_keyboard)
  if current_state == ApplicationState.seccond_step:
    await push_chain_link(state, application_theerd_step)
    await state.set_state(ApplicationState.theerd_step)
    return await callback.message.answer(application_answers["leave_theerd_step"], reply_markup=back_keyboard)
