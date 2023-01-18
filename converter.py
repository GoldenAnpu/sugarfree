def mg_to_mmol(value: int) -> float:
    result = value / 18
    return result


def mmol_to_mg(value: float) -> int:
    result = int(value * 18)
    return result
