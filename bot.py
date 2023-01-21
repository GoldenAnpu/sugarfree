import os
from converter import Units
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import MainMenu
from bot_logger import UserLog

API_TOKEN = os.environ['SUGARFREE_KEY']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def show_welcome(message: types.Message, state: FSMContext):
    user = UserLog(message)
    user.log_action('start')
    lets_go = types.InlineKeyboardButton(text="Let's go!", callback_data="to_main")
    inline_keyboard = types.InlineKeyboardMarkup().add(lets_go)
    await bot.send_message(message.chat.id, text=f"Hi *{user.user_full_name}*!"
                                                 f"\n\nI'm *Sugarfree Bot*!"
                                                 f"\nI'll help you to make your daily life with diabetes easy!",
                           reply_markup=inline_keyboard,
                           parse_mode='Markdown')
    await state.set_state(MainMenu.main_menu)
    user.log_action('state_main_menu_set')


@dp.callback_query_handler(text=["to_main"], state="*")
async def show_welcome(call: types.CallbackQuery):
    user = UserLog(call)
    user.log_action('main_menu')
    convert_button = types.InlineKeyboardButton(text="🧪 Units converter", callback_data="convert")
    info_button = types.InlineKeyboardButton(text="ℹ Information", callback_data="info")
    inline_keyboard = types.InlineKeyboardMarkup().add(convert_button, info_button)
    await call.message.delete()
    await call.message.answer(text="This is the main menu where you can find a section with tool or information to "
                                   "help solve your issue."
                                   "\nChoose the one you want to continue!",
                              reply_markup=inline_keyboard,
                              parse_mode='Markdown')


@dp.callback_query_handler(text=["convert"], state="*")
async def choose_units(call: types.CallbackQuery, state: FSMContext):
    user = UserLog(call)
    user.log_action('convert_menu')
    to_mmol = types.InlineKeyboardButton(text="🩸 mmol/l", callback_data="to_mmol")
    to_mg = types.InlineKeyboardButton(text="🩸 mg/dl", callback_data="to_mg")
    back = types.InlineKeyboardButton(text="🔙 Back", callback_data="to_main")
    inline_keyboard_units = types.InlineKeyboardMarkup().add(to_mmol, to_mg, back)
    await call.message.delete()
    await call.message.answer("Let's start conversion!"                              
                              "\n⚠️Currently you have only two options:"
                              "\n* • mg/dl - mmol/l*"
                              "\n* • mmol/l - mg/dl*"
                              "\n\nChoose *target units*.",
                              reply_markup=inline_keyboard_units,
                              parse_mode='Markdown')
    await state.set_state(MainMenu.converting_units)


@dp.callback_query_handler(text=["to_mmol", "to_mg"], state=MainMenu.converting_units)
async def name_units(call: types.CallbackQuery, state: FSMContext):
    user = UserLog(call)
    user.log_action('choose_units')
    if call.data == "to_mmol":
        units = 'mg/dl to mmol/l'
        await state.set_state(MainMenu.converting_units_to_mmol)
        user.log_action('state_converting_units_to_mmol_set')
        await call.answer("to_mmol")
    else:
        units = 'mmol/l to mg/dl'
        await state.set_state(MainMenu.converting_units_to_mg)
        user.log_action('state_converting_units_to_mg_set')
        await call.answer("to_mg")
    await call.message.delete()
    await call.message.answer(f'*Your choice:* {units}'
                              f'\n\nWrite down your glucometer test results '
                              'than I\'ll convert it for you!',
                              parse_mode='Markdown')


@dp.message_handler(state=MainMenu.converting_units_to_mmol)
async def get_results(message: types.Message):
    user = UserLog(message)
    back = types.InlineKeyboardButton(text="🔙 Change units", callback_data="convert", state=None)
    inline_keyboard_units = types.InlineKeyboardMarkup().add(back)
    try:
        result_1 = Units(int(message.text)).convert_mg_to_mmol()
        result_1 = round(result_1, 2)
        await bot.send_message(message.chat.id, f'*Your blood glucose:* {result_1} mmol/l',
                               parse_mode='Markdown',
                               reply_markup=inline_keyboard_units)
    except ValueError:
        await bot.send_message(message.chat.id, f'Looks like you *made mistake* typing!'
                                                f'\nWrong number: *{message.text}*'
                                                f'\nPlease write down again',
                               parse_mode='Markdown',
                               reply_markup=inline_keyboard_units)
    user.log_action('units_converted_to_mmol')


@dp.message_handler(state=MainMenu.converting_units_to_mg)
async def get_results(message: types.Message):
    user = UserLog(message)
    back = types.InlineKeyboardButton(text="🔙 Change units", callback_data="convert", state=None)
    inline_keyboard_units = types.InlineKeyboardMarkup().add(back)
    try:
        result_2 = Units(float(message.text)).convert_mmol_to_mg()
        result_2 = round(result_2, 2)
        await bot.send_message(message.chat.id, f'*Your blood glucose:* {result_2} mg/dl',
                               parse_mode='Markdown',
                               reply_markup=inline_keyboard_units)
    except ValueError:
        await bot.send_message(message.chat.id, f'Looks like you *made mistake* typing!'
                                                f'\nWrong number: *{message.text}*'
                                                f'\nPlease write down again',
                               parse_mode='Markdown',
                               reply_markup=inline_keyboard_units)
    user.log_action('units_converted_to_mg')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
