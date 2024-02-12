from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from bot.loader.loader import dp
from bot.utils.misc import rate_limit


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("help"))
async def start(message: Message):
    await message.answer("Choose location and answer questions💬\n"
                         "- You can skip or answer✅\n")