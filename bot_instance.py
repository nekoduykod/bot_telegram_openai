from aiogram import Bot

from token_api import TOKEN_API

# Створює бот інстанс. parse_mode='HTML' => щоб ваше ім'я при привітанні було читабельне
bot = Bot(
    token=TOKEN_API,
    parse_mode='HTML'
)