from aiogram.dispatcher.filters.state import State, StatesGroup


class Loc4Form(StatesGroup):
    Location4 = State()
    Item1 = State()
    Item1_comment = State()
    Item2 = State()
    Item2_comment = State()
    Item3 = State()
    Item3_comment = State()
    Item4 = State()
    Item4_comment = State()
    Item5 = State()
    Item5_comment = State()
    Photo = State()
    Photo_processing = State()