from aiogram import Bot

from token_api import TOKEN_API

# Створює бот інстанс
bot = Bot(
    token=TOKEN_API,
    parse_mode='HTML'
)