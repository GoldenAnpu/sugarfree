
class Converter:
    def __init__(self, initializer):
        self.initializer = initializer
        self.value = initializer.text
        self.units = None
        self.result = None

        if ',' in self.value:
            self.value = self.value.replace(',', '.')
        if '.' in self.value:
            self.value = float(self.value)
        else:
            self.value = int(self.value)

    def convert_mg_to_mmol(self) -> float:
        self.result = self.value / 18
        self.units = 'mmol/l'
        return self.result

    def convert_mmol_to_mg(self) -> int:
        self.result = int(self.value * 18)
        self.units = 'mg/dl'
        return self.result

    def make_conversion(self, state, inline_keyboard_units):
        if state == 'converting_units_to_mmol':
            result = round(self.convert_mg_to_mmol(), 2)
        elif state == 'converting_units_to_mg':
            result = self.convert_mmol_to_mg()
        else:
            result = "err"
        return self.initializer.answer(f'*Your blood glucose:* {result} {self.units}',
                                       parse_mode='Markdown',
                                       reply_markup=inline_keyboard_units)
