import os
import logging
import time
import aiogram.types
import aiogram.utils.exceptions as Exceptions
from aiogram import Bot, Dispatcher, executor, types
import converter

API_TOKEN = os.environ['SUGARFREE_KEY']


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def logging(user_id, user_full_name):
    return logging.info(f'{user_id} {user_full_name} {time.asctime()}')


def get_user_info(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    return user_id, user_name, user_full_name


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_info = get_user_info(message)
    # logging(user_info[0], user_info[2])
    convert_button = types.InlineKeyboardButton(text="🧪 Units converter", callback_data="convert")
    inline_keyboard = types.InlineKeyboardMarkup().add(convert_button)
    await bot.send_message(message.chat.id, text=f"Hi {user_info[2]}!"
                                                 f"\nI'm Sugarfree Bot!"
                                                 f"\nI'll help you to make your daily life with diabetes easy!",
                           reply_markup=inline_keyboard)


@dp.callback_query_handler(text=["convert"])
async def choose_units(call: types.CallbackQuery):

    if call.data == "convert":
        to_mmol = types.InlineKeyboardButton(text="🩸 mg/dl to mmol/l", callback_data="to_mmol")
        to_mg = types.InlineKeyboardButton(text="🩸 mmol/l to mg/dl", callback_data="to_mg")
        inline_keyboard_units = types.InlineKeyboardMarkup().add(to_mmol, to_mg)
        await call.message.answer("Great.. Let's start conversion!\nChoose conversion type!",
                                  reply_markup=inline_keyboard_units)


@dp.callback_query_handler(text=["to_mmol", "to_mg"])
async def convert_units(call: types.CallbackQuery):
    if call.data == "to_mmol":
        await call.message.delete()
        await call.message.answer('*Your choice:* mg/dl to mmol/l\nWrite down your glucometer test results'
                                  '\nThan I\'ll convert it for you!',
                                  parse_mode=aiogram.types.ParseMode.MARKDOWN)

        @dp.message_handler()
        async def get_result_mmol(message: types.Message):
            back = types.InlineKeyboardButton(text="🔙 Change units", callback_data="convert")
            inline_keyboard_units = types.InlineKeyboardMarkup().add(back)
            result_1 = converter.mg_to_mmol(int(message.text))
            result_1 = round(result_1, 2)
            await call.message.answer(f'*Your sugar level:* {result_1} mmol/l',
                                      parse_mode=aiogram.types.ParseMode.MARKDOWN,
                                      reply_markup=inline_keyboard_units)

    elif call.data == "to_mg":
        await call.message.delete()
        await call.message.answer('*Your choice:* mmol/l to mg/dl\nWrite down your glucometer test results'
                                  '\nThan I\'ll convert it for you!',
                                  parse_mode=aiogram.types.ParseMode.MARKDOWN)

        @dp.message_handler()
        async def get_result_mg(message: types.Message):
            back = types.InlineKeyboardButton(text="🔙 Change units", callback_data="convert")
            inline_keyboard_units = types.InlineKeyboardMarkup().add(back)
            result_2 = converter.mg_to_mmol(int(message.text))
            result_2 = round(result_2, 2)
            await call.message.answer(f'*Your sugar level:* {result_2} mg/dl',
                                      parse_mode=aiogram.types.ParseMode.MARKDOWN,
                                      reply_markup=inline_keyboard_units)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
