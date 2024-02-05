import logging
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


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Кожен атрибут класу - це "стейт", в якому бот можу бути при діалозі. Очікує відповідь користувача. 
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


# Вітання
@dp.message_handler(Command('start'))
async def welcome(message: types.Message, state: FSMContext) -> None:
    """ The command 'start' """
    reply_text = f'{hbold(message.from_user.first_name)}, ласкаво прошу. Почнімо. Оберіть локацію, що вас цікавить.'

    await bot.send_message(
        message.chat.id,
        text=reply_text,
        reply_markup=locations_kb.menu
    )
    await ChecklistForm.Location.set()


''' 
Якщо додати 'Location 2-5' -> скопіюй в handler.py всі Items + 4 рази, але з різними назвами функцій (уникнення конфліктів),
та StatesGroup. + handler з if message.text == 'Location 1': ... , ...=='Location 2': так далі, що створить +1000
рядків коду. Вирішив залишити Location 1 з його 6-ма checklist. Розбиваючи по файлах loc1_handler.py, loc2.py,
loc3.py... - не переходило в next стейт, допоки не копіював state snippets саме в handler.py. Лише тоді воно бачило їх.
Цікаво, чи дозволяє aiogram 2.25 розбивати на файли StatesGroups. Напевно, версія aiogram 3.3+ .
'''
# Обирай Локацію з locations_kb.menu.
@dp.message_handler(lambda message: message.text == 'Location 1', state=ChecklistForm.Location)
async def choose_location(message: types.Message, state: FSMContext):
    location = message.text
    await state.update_data(location=location)

    await bot.send_message(message.chat.id, text=f"{location}. Мерщій заповни чекліст!", reply_markup=types.ReplyKeyboardRemove())

    await bot.send_message(message.chat.id, text="Item 1 => Пропустити - введіть цифру 1 | Залишити коментар - 2.")
    await ChecklistForm.Item1.set()


# Чек 1
@dp.message_handler(state=ChecklistForm.Item1)
async def process_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(ChecklistForm.Item2) # або => await ChecklistForm.Item2.set()
       await bot.send_message(message.chat.id, text="Item 2 => Пропустити - 1  | Залишити коментар - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(ChecklistForm.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ніт, лише цифра 1 чи 2, будь ласка.")

@dp.message_handler(state=ChecklistForm.Item1_comment)
async def process_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text="Item 2 => Пропустити - введіть 1 | Залишити комент - 2.")
    await ChecklistForm.next()


# Чек 2
@dp.message_handler(state=ChecklistForm.Item2)
async def process_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await ChecklistForm.Item3.set()
        await bot.send_message(message.chat.id, text="Item 3 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(ChecklistForm.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ше раз! 1 чи 2")

@dp.message_handler(state=ChecklistForm.Item2_comment)
async def process_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text="Item 3 => Пропустити - цифра(5 мінус 4) | Залишити комент - цифра(корінь з чотирьох)")
    await ChecklistForm.next()


# Чек 3
@dp.message_handler(state=ChecklistForm.Item3)
async def process_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await ChecklistForm.Item4.set()
        await bot.send_message(message.chat.id, text="Item 4 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(ChecklistForm.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ойой! 1, чи 2")

@dp.message_handler(state=ChecklistForm.Item3_comment)
async def process_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text="Item 4 => Лінь відповісти - 1 | Залишити коментар - 2.")
    await ChecklistForm.next()


# Чек 4
@dp.message_handler(state=ChecklistForm.Item4)
async def process_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await ChecklistForm.Item5.set()
        await bot.send_message(message.chat.id, text="Item 5 => Пропустити - арабська один | Залиш коментар - цифра два.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(ChecklistForm.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text="Арабська 1, чи 2 !")

@dp.message_handler(state=ChecklistForm.Item4_comment)
async def process_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text="Item 5 => Пропустити - 1 | Залишити коментар - 2.")
    await ChecklistForm.next()


# Чек 5
@dp.message_handler(state=ChecklistForm.Item5)
async def process_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await ChecklistForm.Photo.set()
        await bot.send_message(message.chat.id, text="Залиште URL на фото. Пропустити - 1. Залишити - 2")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(ChecklistForm.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text="Промах по клавіатурі detected. 1, чи 2 !")

@dp.message_handler(state=ChecklistForm.Item5_comment)
async def process_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text="Залиште URL на фото, що стосується питання. Ніт - 1. Так - 2")
    await ChecklistForm.next()


# Чек 6 (фото)
@dp.message_handler(state=ChecklistForm.Photo)
async def photo_url(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(photo_url_reponse='Skip')
        await bot.send_message(message.chat.id, text="Усьо! Обробляємо. Покірно почекайте, будь ласка.")
        await process_checklist_and_send_report(state)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште URL")
        await state.set_state(ChecklistForm.Photo_processing)
        await state.update_data(photo_url_reponse=None)
    else:
        await bot.send_message(message.chat.id, text="9, чи 10? Ne chue baba. Повторіть, будь ласка.")

@dp.message_handler(state=ChecklistForm.Photo_processing)
async def photo_url_processing(message: types.Message, state: FSMContext):
    await state.update_data(photo_url_reponse=message.text)

    await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка запиту. Стривайте.")
    await process_checklist_and_send_report(state)


# Обробка/відправка ChatGPT, та назад користувачу. Цей шмат коду можна перенести в інший file.py за бажанням.
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
        print(data)  # {'location': 'Location 1', 'item1_response': 'Skip', 'item2_response': 'comment 2', 'item3_response': 'com3', 'item4_response': 'com4', 'item5_response': 'com5', 'photo_url_reponse': 'http://photo.com'}
        data_string = json.dumps(data)

        prompt_text = "Analyze the following questions/data:"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt_text + data_string,
            max_tokens=1000  # ліміт за бажанням/бюджетом
        )
        # Обробляє відповідь ChatGPT
        chatgpt_response = response.choices[0].text.strip()

        await bot.send_message(state.user, text=chatgpt_response)
        await bot.send_message(state.user, text="Дякую. Сонячного дня! Звертайтесь.")
        # Очищує дані, скидує на початковий стан
        await state.finish()

    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API Error: {e}")
        await bot.send_message(state.user, text="Халепа. Перепрошую. Над проблемою працюють, зверніться пізніше.")

    except Exception as e:
        logging.exception(f"Unexpected Error: {e}")
        await bot.send_message(state.user, text="Йой! Технічні проблеми. Буль ласка, зверніться пізніше.")