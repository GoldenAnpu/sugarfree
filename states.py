from aiogram.dispatcher.filters.state import StatesGroup, State


class MainMenu(StatesGroup):
    start = State()
    main_menu = State()
    getting_info = State()
    converting_units = State()
    converting_units_to_mmol = State()
    converting_units_to_mg = State()
