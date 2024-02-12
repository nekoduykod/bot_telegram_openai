from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


menu = ReplyKeyboardMarkup(resize_keyboard=True).row(
            KeyboardButton("Location 1"),
            KeyboardButton("Location 2"),
            KeyboardButton("Location 3"),
            KeyboardButton("Location 4")
)

inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True).add(
    InlineKeyboardButton(text="Location 1", callback_data="location_1"),
    InlineKeyboardButton(text="Location 2", callback_data="location_2"),
    InlineKeyboardButton(text="Location 3", callback_data="location_3"),
    InlineKeyboardButton(text="Location 4", callback_data="location_4")
)   