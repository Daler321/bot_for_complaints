from aiogram import types

from config import texts as answers

contact_keyboard_text = answers["keyboards"]["contact_keyboards"]
back_text = answers["keyboards"]["back_btn"]

contact_keyboard_buttons = [
  [types.InlineKeyboardButton(text=contact_keyboard_text["call"], callback_data='call')],
  [types.InlineKeyboardButton(text=contact_keyboard_text["chat"], callback_data='chat')],
  [types.InlineKeyboardButton(text=back_text, callback_data='back')]
]

contact_keyboard = types.InlineKeyboardMarkup(inline_keyboard=contact_keyboard_buttons)

is_right_number_buttons = [
  [types.InlineKeyboardButton(text=contact_keyboard_text["yes"], callback_data='yes'), types.InlineKeyboardButton(text=contact_keyboard_text["leave_number"], callback_data='leave_number')]
]

is_right_number_keyboard = types.InlineKeyboardMarkup(inline_keyboard=is_right_number_buttons)

chat_buttons = [
  [types.InlineKeyboardButton(text=contact_keyboard_text["end_chat"], callback_data='end_chat')]
]

chat_keyboard = types.InlineKeyboardMarkup(inline_keyboard=chat_buttons)