from aiogram import types

from config import texts as answers

main_keyboard_text = answers["keyboards"]["main_keyboard"]

main_keyboard_buttons = [
  [types.KeyboardButton(text=main_keyboard_text["leave_application"]), types.KeyboardButton(text=main_keyboard_text["contact"])],
  [types.KeyboardButton(text=main_keyboard_text["settings"])],
  [types.KeyboardButton(text=main_keyboard_text["helpful_contacts"])]
]

main_keyboard = types.ReplyKeyboardMarkup(keyboard=main_keyboard_buttons, resize_keyboard=True)