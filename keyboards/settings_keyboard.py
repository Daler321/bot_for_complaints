from aiogram import types

from config import texts as answers

settings_keyboard_text = answers["keyboards"]["settings_keyboard"]

settings_keyboard_buttons = [
  [types.InlineKeyboardButton(text=settings_keyboard_text["change_name"], callback_data='change_name'), types.InlineKeyboardButton(text=settings_keyboard_text["change_number"], callback_data='change_number')],
  [types.InlineKeyboardButton(text=answers["keyboards"]["back_btn"], callback_data='back')],
]

settings_keyboard = types.InlineKeyboardMarkup(inline_keyboard=settings_keyboard_buttons)