from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery

from main import bot, dp, types
from bot.keyboards.inline import keyboards_menu
# from bot.handlers.users.issues_handler import ChooseLoc
from bot.data.text import welcome_text
# from bot.utils.misc import rate_limit


# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from bot.states.states import ChooseButton, Is, Loc2Form, Loc3Form, Loc4Form

# @rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command('start'))
async def start_cmd(message: types.Message):
    reply_text = f'{hbold(message.from_user.first_name)}, {welcome_text}'
    await bot.send_message(chat_id=message.from_user.id, 
                           text=reply_text)


@dp.message_handler(Command('exit'), state="*")
async def exit_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Exiting...")