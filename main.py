import asyncio

from bot_instance import bot
from bot.handlers.handler import dp

async def main() -> None:
    """it executes the event loop and start polling"""
    await dp.start_polling()

if __name__ == '__main__':
    # starts the bot 
    asyncio.run(main())