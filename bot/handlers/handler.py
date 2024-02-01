import json

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold

from bot_instance import bot
from bot.keyboards import locations_kb

import openai
from token_api import OPENAI_API_KEY


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Кожен атрибут класу - це "стейт", в якому бот можу бути при діалозі. Очікує відповідь користувача
class ChecklistForm(StatesGroup):
    Location = State()
    Item1 = State()
    Item1_comment = State()
    Item2 = State()
    Item2_comment = State()
    Item3 = State()
    Item3_comment = State()
    Item4 = State()
    Item4_comment = State()
    Item5 = State()
    Item5_comment = State()
    Photo = State()
    Photo_processing = State()

# вітання
@dp.message_handler(Command('start'))
async def welcome(message: types.Message, state: FSMContext) -> None:
    """ The command 'start' """
    reply_text = f'{hbold(message.from_user.first_name)}, ласкаво прошу. Почнімо. Оберіть локацію, що вас цікавить, будь ласка.'

    await bot.send_message(
        message.chat.id,
        text=reply_text,
        reply_markup=locations_kb.menu
    )
    await ChecklistForm.Location.set()

# Обирай Локацію з locations_kb.menu. *if 'Location 2-5' - simply copy choose_location code & changie Num ; or using re module if questions same
@dp.message_handler(lambda message: message.text == 'Location 1', state=ChecklistForm.Location)
async def choose_location(message: types.Message, state: FSMContext):
    location = message.text
    await state.update_data(location=location)

    await bot.send_message(message.chat.id, text=f"{location}. Заповніть, будь ласка, чекліст")

    await bot.send_message(message.chat.id, text="Item 1, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    await ChecklistForm.Item1.set()

# чекліст 1
@dp.message_handler(state=ChecklistForm.Item1)
async def process_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 1")
        await state.set_state(ChecklistForm.Item1_comment)
        await state.update_data(item1_response=None)

@dp.message_handler(state=ChecklistForm.Item1_comment)
async def process_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text="Item 2, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    await ChecklistForm.Item2.set()

# чекліст 2
@dp.message_handler(state=ChecklistForm.Item2)
async def process_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 2")
        await state.set_state(ChecklistForm.Item2_comment)
        await state.update_data(item2_response=None)

@dp.message_handler(state=ChecklistForm.Item2_comment)
async def process_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text="Item 3, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    await ChecklistForm.Item3.set()

# чекліст 3
@dp.message_handler(state=ChecklistForm.Item3)
async def process_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 3")
        await state.set_state(ChecklistForm.Item3_comment)
        await state.update_data(item3_response=None)

@dp.message_handler(state=ChecklistForm.Item3_comment)
async def process_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text="Item 4, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    await ChecklistForm.Item4.set()

# чекліст 4
@dp.message_handler(state=ChecklistForm.Item4)
async def process_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 4")
        await state.set_state(ChecklistForm.Item4_comment)
        await state.update_data(item4_response=None)

@dp.message_handler(state=ChecklistForm.Item4_comment)
async def process_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text="Item 5, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    await ChecklistForm.Item5.set()

# чекліст 5
@dp.message_handler(state=ChecklistForm.Item5)
async def process_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 5")
        await state.set_state(ChecklistForm.Item5_comment)
        await state.update_data(item5_response=None)

@dp.message_handler(state=ChecklistForm.Item5_comment)
async def process_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text="Опціонально, залиште лінк на фото, що стосується питання. Пропустіть - 1. Залишити - 2")
    await ChecklistForm.Photo.set()

# чекліст 6, фото
@dp.message_handler(state=ChecklistForm.Photo)
async def photo_url(message: types.Message, state: FSMContext):
    if message.text == '1':
        await process_checklist_and_send_report(state)
    if message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште URL")
        await state.set_state(ChecklistForm.Photo_processing)
        await state.update_data(photo_url_reponse=None)

@dp.message_handler(state=ChecklistForm.Photo_processing)
async def photo_url_processing(message: types.Message, state: FSMContext):
    await state.update_data(photo_url_reponse=message.text)

    await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка Вашого запиту. Зачекайте.")
    await process_checklist_and_send_report(state)

# обробка, відправка чатжпт, і назад користувачу
async def process_checklist_and_send_report(state: FSMContext):
    try:
        data = await state.get_data()
        location = data.get('location')
        checklist_responses = [
            data.get('item1_response'),
            data.get('item2_response'),
            data.get('item3_response'),
            data.get('item4_response'),
            data.get('item5_response'),
            data.get('photo_url_reponse')
        ]
        print(data)  # {'location': 'Location 1', 'item1_response': '1', 'item2_response': 'asdasd', 'item3_response': 'asdasdd', 'item4_response': 'com4', 'item5_response': 'com5', 'photo_url_reponse': 'http://photo.com'}
        data_string = json.dumps(data)

        prompt_text = "Analyze the following questions/data:"

        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text + data_string,
        max_tokens=60  # тест короткою відповіддю
        )
        # Обробляє відповідь ChatGPT
        chatgpt_response = response.choices[0].text.strip()

        await bot.send_message(state.user, text=chatgpt_response)
        await bot.send_message(state.user, text="Дякую. Гарного дня! звертайтесь.")
        # очишує дані, скидує стан бота на початк. стан
        await state.finish()

    except openai.error.OpenAIError as e:
        # можна для винятків, замість print, logging використовувати
        print(f"OpenAI API Error: {e}")
        await bot.send_message(state.user, text="Oops! Something went wrong while processing your request. Please try again later.")

    except Exception as e:
        print(f"Unexpected Error: {e}")
        await bot.send_message(state.user, text="Oops! Something unexpected happened. Please try again later.")