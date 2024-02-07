import asyncio

from aiogram import Bot
from aiogram import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .config import TOKEN_API


bot = Bot(
    token=TOKEN_API,
    parse_mode='HTML'
)


storage = MemoryStorage() 
dp = Dispatcher(bot, storage=storage)


async def main() -> None:
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())