from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from bot.loader.loader import bot, dp
from bot.keyboards import keyboards_menu
from bot.states.states import ChooseLoc
from bot.data.text import welcome_text
from bot.utils.misc import rate_limit


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command('start'))
async def welcome(message: Message, state: FSMContext) -> None:
    """ command '/start' """
    reply_text = f'{hbold(message.from_user.first_name)}, {welcome_text}'

    await bot.send_message(
        message.chat.id,
        text=reply_text,
        reply_markup=keyboards_menu.menu
    )
    await ChooseLoc.Location.set()