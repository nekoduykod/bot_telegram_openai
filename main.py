import asyncio

from bot_instance import bot
from aiogram import executor

from bot.handlers.handler import dp

async def main() -> None:
    """It will execute our event loop and start polling."""
    await dp.start_polling()

if __name__ == '__main__':
    # Start the bot 
    asyncio.run(main())