import asyncio

from aiogram import Dispatcher

from bot_instance import bot
from bot.handlers.user_handlers import user_router


def register_routers(dp: Dispatcher) -> None:
    """it registers routers"""

    dp.include_router(user_router)


async def main() -> None:
    """it will execute our event loop and start polling."""
    
    dp = Dispatcher()

    register_routers(dp)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    # starts the bot 
    asyncio.run(main())