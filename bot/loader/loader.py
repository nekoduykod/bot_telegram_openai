import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# from utils.db_api.postgresql import Database
from bot.data.config import BOT_TOKEN
from bot.utils.set_bot_commands import set_default_commands


bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage() 
dp = Dispatcher(bot, storage=storage)

async def on_startup(dp):
    from utils.notify_admins import on_startup_notify

    import middlewares
    middlewares.setup(dp)
    await set_default_commands(dp)
    await on_startup_notify(dp)

async def on_shutdown(dp):
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)
    await bot.close()

# loop = asyncio.get_event_loop()
# db = loop.run_until_complete(Database.create())

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)