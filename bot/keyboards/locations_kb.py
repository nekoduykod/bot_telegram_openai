from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(resize_keyboard=True).row(
            KeyboardButton("Location 1"),
            KeyboardButton("Location 2"),
            KeyboardButton("Location 3"),
            KeyboardButton("Location 4"),
            KeyboardButton("Location 5")
)