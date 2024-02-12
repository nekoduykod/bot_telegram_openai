from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


menu = ReplyKeyboardMarkup(resize_keyboard=True).row(
            KeyboardButton("/start"),
            KeyboardButton("/exit") # вийти з Location checlist на головне меню
)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True).add(
            InlineKeyboardButton(text="Location 1", callback_data="1"),
            InlineKeyboardButton(text="Location 2", callback_data="2"),
            InlineKeyboardButton(text="Location 3", callback_data="3"),
            InlineKeyboardButton(text="Location 4", callback_data="4")
)