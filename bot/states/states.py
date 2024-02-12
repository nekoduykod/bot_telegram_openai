from aiogram.dispatcher.filters.state import State, StatesGroup


class ChooseLoc(StatesGroup):
    Location = State()

class Loc1Form(StatesGroup):
    Location1 = State()
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

class Loc2Form(StatesGroup):
    Location2 = State()
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

class Loc3Form(StatesGroup):
    Location3 = State()
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

class LeavePhoto(StatesGroup):
    URL = State()
    URL_processing = State()