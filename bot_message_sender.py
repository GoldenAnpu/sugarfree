from aiogram import types


class BotMessage:
    def __init__(self, initializer: [types.Message, types.CallbackQuery], keyboard=None):
        self.initializer = initializer
        self.keyboard = keyboard

    def send_message_mistake_in_glucose_value(self):
        return self.initializer.answer(f'Looks like you *made mistake* typing!'
                                       f'\nWrong number: *{self.initializer.text}*'
                                       f'\nPlease write down again',
                                       parse_mode='Markdown',
                                       reply_markup=self.keyboard)

    def send_message_with_defined_units(self):
        if self.initializer.data == "to_mmol":
            units = 'mg/dl to mmol/l'
        else:
            units = 'mmol/l to mg/dl'
        return self.initializer.message.answer(f'*Your choice:* {units}'
                                               f'\n\nWrite down your glucometer test results '
                                               'than I\'ll convert it for you!',
                                               parse_mode='Markdown')

    def send_message_start_conversion(self):
        return self.initializer.message.answer("Let's start conversion!"
                                               "\nCurrently, you only have two options:"
                                               "\n* • mg/dl - mmol/l*"
                                               "\n* • mmol/l - mg/dl*"
                                               "\n\nPlease select *target units*.",
                                               reply_markup=self.keyboard,
                                               parse_mode='Markdown')

    def send_message_main_menu_descr(self):
        return self.initializer.message.answer(text="This is the main menu where you can find tools or information"
                                                    " to help you solve your issue."
                                                    "\nSelect the one you want to proceed with!",
                                               reply_markup=self.keyboard,
                                               parse_mode='Markdown')

    def send_message_show_welcome(self):
        return self.initializer.answer(text=f"Hi *{self.initializer.from_user.full_name}*!"
                                            f"\n\nI'm *Sugarfree Bot*!"
                                            f"\nI'll assist you in making daily life with diabetes manageable!",
                                       reply_markup=self.keyboard,
                                       parse_mode='Markdown')
