from aiogram import types

from config import texts as answers

application_keyboard_text = answers["keyboards"]["application_keyboard"]
back_text = answers["keyboards"]["back_btn"]

application_keyboard_buttons = [
  [types.InlineKeyboardButton(text=application_keyboard_text["leave_application"], callback_data='application'), types.InlineKeyboardButton(text=application_keyboard_text["offer"], callback_data='offer')],
  [types.InlineKeyboardButton(text=back_text, callback_data='back')]
]

application_keyboard = types.InlineKeyboardMarkup(inline_keyboard=application_keyboard_buttons)

back_buttons = [
  [types.InlineKeyboardButton(text=back_text, callback_data='back')]
]

back_keyboard = types.InlineKeyboardMarkup(inline_keyboard=back_buttons)

back_skip_buttons = [
  [types.InlineKeyboardButton(text=application_keyboard_text["skip"], callback_data='skip')],
  [types.InlineKeyboardButton(text=back_text, callback_data='back')]
]

back_skip_keyboard = types.InlineKeyboardMarkup(inline_keyboard=back_skip_buttons)