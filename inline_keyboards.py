from aiogram import types

# predefined buttons
lets_go = types.InlineKeyboardButton(text="Let's go!", callback_data="to_main")
convert_button = types.InlineKeyboardButton(text="๐งช Units converter", callback_data="convert")
info_button = types.InlineKeyboardButton(text="โน Information", callback_data="info")
to_mmol = types.InlineKeyboardButton(text="๐ฉธ mmol/l", callback_data="to_mmol")
to_mg = types.InlineKeyboardButton(text="๐ฉธ mg/dl", callback_data="to_mg")
back = types.InlineKeyboardButton(text="๐ Back", callback_data="to_main")
change_units = types.InlineKeyboardButton(text="๐ Change units", callback_data="convert")

# list of buttons for def main_menu_keyboard
main_menu_keyboard = [convert_button, info_button]

# list of buttons for def choose_units
choose_units_keyboard = [to_mmol, to_mg, back]
