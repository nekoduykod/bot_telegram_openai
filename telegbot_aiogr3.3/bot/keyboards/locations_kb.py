from aiogram.utils.keyboard import ReplyKeyboardBuilder


# def keyboard():
menu = ReplyKeyboardBuilder().button(text="Location 1").button(text="Location 2") \
.button(text="Location 3").button(text="Location 4").button(text="Location 5").as_markup()