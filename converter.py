class Units:
    def __init__(self, value):
        self.value = value

    def convert_mg_to_mmol(self) -> float:
        result = self.value / 18
        return result

    def convert_mmol_to_mg(self) -> int:
        result = int(self.value * 18)
        return result
