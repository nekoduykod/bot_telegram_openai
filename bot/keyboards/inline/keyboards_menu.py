from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


menu = ReplyKeyboardMarkup(resize_keyboard=True).row(
            KeyboardButton("/start"),
            KeyboardButton("/exit")
)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True).add(
            InlineKeyboardButton(text="Location 1", callback_data="Loc1"),
            InlineKeyboardButton(text="Location 2", callback_data="Loc2"),
            InlineKeyboardButton(text="Location 3", callback_data="Loc3"),
            InlineKeyboardButton(text="Location 4", callback_data="Loc4")
)