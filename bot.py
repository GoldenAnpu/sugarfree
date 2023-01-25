import os
import inline_keyboards as buttons
from unit_converter import Converter
from aiogram import Bot, Dispatcher, executor, types
from state_controller import Database
from state_controller import States
from bot_message_sender import BotMessage
from action_logger import UserLog
from aiogram.utils.exceptions import MessageToDeleteNotFound

API_TOKEN = os.environ['SUGARFREE_KEY']
BOT_MESSAGE_ID = 0

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = Database()


@dp.message_handler(commands=['start'])
async def show_welcome(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup().add(buttons.lets_go)
    await BotMessage(message, inline_keyboard).send_message_show_welcome()
    db.set_state(message.from_user.id, States.main_menu)
    UserLog(message).log_action('Bot started. States main_menu has been set.')


@dp.callback_query_handler(text=["to_main"])
async def show_main_menu(call: types.CallbackQuery):
    inline_keyboard = types.InlineKeyboardMarkup().add(*buttons.main_menu_keyboard)
    await call.message.delete()
    await BotMessage(call, inline_keyboard).send_message_main_menu_descr()
    UserLog(call).log_action('Entered the main menu')


@dp.callback_query_handler(text=["convert"])
async def choose_units(call: types.CallbackQuery):
    inline_keyboard = types.InlineKeyboardMarkup().add(*buttons.choose_units_keyboard)
    await call.message.delete()
    await BotMessage(call, inline_keyboard).send_message_start_conversion()
    db.set_state(call.from_user.id, States.converting_units)
    UserLog(call).log_action('State changed to converting_units. User navigated to the unit selection menu.')


@dp.callback_query_handler(text=["to_mmol", "to_mg"])
async def name_units(call: types.CallbackQuery):
    if db.get_state(call.from_user.id) == States.converting_units:
        if call.data == "to_mmol":
            db.set_state(call.from_user.id, States.converting_units_to_mmol)
            UserLog(call).log_action('State changed to converting_units_to_mmol. Ready to receive values.')
        elif call.data == "to_mg":
            db.set_state(call.from_user.id, States.converting_units_to_mg)
            UserLog(call).log_action('State changed to converting_units_to_mg. Ready to receive values.')
        await call.message.delete()
        message = await BotMessage(call).send_message_with_defined_units()
        global BOT_MESSAGE_ID
        BOT_MESSAGE_ID = message.message_id


@dp.message_handler()
async def get_results(message: types.Message):
    current_state = db.get_state(message.from_user.id)
    if current_state in [States.converting_units_to_mmol,
                         States.converting_units_to_mg]:
        try:
            await bot.delete_message(message.chat.id, BOT_MESSAGE_ID)
        except MessageToDeleteNotFound:
            pass
        inline_keyboard = types.InlineKeyboardMarkup().add(buttons.change_units)
        try:
            await Converter(message).make_conversion(current_state, inline_keyboard)
        except ValueError:
            await BotMessage(message, inline_keyboard).send_message_mistake_in_glucose_value()
        UserLog(message).log_action('Unit conversion has occurred.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
