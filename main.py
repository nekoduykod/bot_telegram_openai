import asyncio

from bot.handlers.menu import dp


async def main() -> None:
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())