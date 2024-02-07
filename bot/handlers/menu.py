import re

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher import FSMContext

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold

from bot_instance import bot
from bot.keyboards import locations_kb

from ..states.states import ChooseLoc, Loc1Form, Loc2Form, Loc3Form, Loc4Form, Loc5Form
from ..functions.request_chatgpt import process_checklist_and_send_report


storage = MemoryStorage()    # TODO this must be separate   # TODO text/data = separate, code = separate
dp = Dispatcher(bot, storage=storage)


# Вітання
@dp.message_handler(Command('start'))
async def welcome(message: types.Message, state: FSMContext) -> None:
    """ command '/start' """
    reply_text = f'{hbold(message.from_user.first_name)}, ласкаво прошу. Почнімо. Оберіть локацію, що вас цікавить.'

    await bot.send_message(
        message.chat.id,
        text=reply_text,
        reply_markup=locations_kb.menu
    )
    await ChooseLoc.Location.set()


# Обирай Локацію з locations_kb.menu.
@dp.message_handler(lambda message: bool(re.match("^Location [1-5]$", message.text)), state=ChooseLoc.Location)
async def handle_location(message: types.Message, state: FSMContext):
    location = message.text
    await state.update_data(location=location)
    await bot.send_message(message.chat.id, text=f"{location}. Мерщій заповни чекліст.",
                            reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, text="Item 1 => Пропустити - 1  | Залишити коментар - 2.")
    if message.text == 'Location 1':
        await state.set_state(Loc1Form.Item1)
    elif message.text == 'Location 2':
        await state.set_state(Loc2Form.Item1)
    elif message.text == 'Location 3':
        await state.set_state(Loc3Form.Item1)
    elif message.text == 'Location 4':
        await state.set_state(Loc4Form.Item1)
    elif message.text == 'Location 5':
        await state.set_state(Loc5Form.Item1)


# Чек 1 Лок 1
@dp.message_handler(state=Loc1Form.Item1)
async def process_loc1_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Loc1Form.Item2) # або => await Loc1Form.Item2.set()
       await bot.send_message(message.chat.id, text="Item 2 => Пропустити - 1  | Залишити коментар - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc1Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ніт, лише цифра 1 чи 2, будь ласка.")

@dp.message_handler(state=Loc1Form.Item1_comment)
async def process_loc1_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text="Item 2 => Пропустити - введіть 1 | Залишити комент - 2.")
    await Loc1Form.next()


# Чек 2 Лок 1
@dp.message_handler(state=Loc1Form.Item2)
async def process_loc1_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc1Form.Item3.set()
        await bot.send_message(message.chat.id, text="Item 3 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc1Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ше раз! 1 чи 2")

@dp.message_handler(state=Loc1Form.Item2_comment)
async def process_loc1_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text="Item 3 => Пропустити - цифра(5 мінус 4) | Залишити комент - цифра(корінь з чотирьох)")
    await Loc1Form.next()


# Чек 3 Лок 1
@dp.message_handler(state=Loc1Form.Item3)
async def process_loc1_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc1Form.Item4.set()
        await bot.send_message(message.chat.id, text="Item 4 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc1Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ойой! 1, чи 2")

@dp.message_handler(state=Loc1Form.Item3_comment)
async def process_loc1_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text="Item 4 => Лінь відповісти - 1 | Залишити коментар - 2.")
    await Loc1Form.next()


# Чек 4 Лок 1
@dp.message_handler(state=Loc1Form.Item4)
async def process_loc1_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc1Form.Item5.set()
        await bot.send_message(message.chat.id, text="Item 5 => Пропустити - арабська один | Залиш коментар - цифра два.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc1Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text="Арабська 1, чи 2 !")

@dp.message_handler(state=Loc1Form.Item4_comment)
async def process_loc1_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text="Item 5 => Пропустити - 1 | Залишити коментар - 2.")
    await Loc1Form.next()


# Чек 5 Лок 1
@dp.message_handler(state=Loc1Form.Item5)
async def process_loc1_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await Loc1Form.Photo.set()
        await bot.send_message(message.chat.id, text="Залиште URL на фото. Пропустити - 1. Залишити - 2")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc1Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text="Промах по клавіатурі detected. 1, чи 2 !")

@dp.message_handler(state=Loc1Form.Item5_comment)
async def process_loc1_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text="Залиште URL на фото, що стосується питання. Ніт - 1. Так - 2")
    await Loc1Form.next()


# Чек 6 (фото) Лок 1
@dp.message_handler(state=Loc1Form.Photo)
async def photo_loc1_url(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(photo_url_reponse='Skip')
        await bot.send_message(message.chat.id, text="Усьо! Обробляємо. Покірно почекайте, будь ласка.")
        await process_checklist_and_send_report(state)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште URL")
        await state.set_state(Loc1Form.Photo_processing)
        await state.update_data(photo_url_reponse=None)
    else:
        await bot.send_message(message.chat.id, text="9, чи 10? Ne chue baba. Повторіть, будь ласка.")

@dp.message_handler(state=Loc1Form.Photo_processing)
async def photo_loc1_url_processing(message: types.Message, state: FSMContext):
    await state.update_data(photo_url_reponse=message.text)

    await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка запиту. Стривайте.")
    await process_checklist_and_send_report(state)


# Чек 1 Лок 2
@dp.message_handler(state=Loc2Form.Item1)
async def process_loc2_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Loc2Form.Item2)
       await bot.send_message(message.chat.id, text="Item 2 => Пропустити - 1  | Залишити коментар - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc2Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ніт, лише цифра 1 чи 2, будь ласка.")

@dp.message_handler(state=Loc2Form.Item1_comment)
async def process_loc2_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text="Item 2 => Пропустити - введіть 1 | Залишити комент - 2.")
    await Loc2Form.next()


# Чек 2 Лок 2
@dp.message_handler(state=Loc2Form.Item2)
async def process_loc2_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc2Form.Item3.set()
        await bot.send_message(message.chat.id, text="Item 3 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc2Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ше раз! 1 чи 2")

@dp.message_handler(state=Loc2Form.Item2_comment)
async def process_loc2_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text="Item 3 => Пропустити - цифра(5 мінус 4) | Залишити комент - цифра(корінь з чотирьох)")
    await Loc2Form.next()


# Чек 3 Лок 2
@dp.message_handler(state=Loc2Form.Item3)
async def process_loc2_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc2Form.Item4.set()
        await bot.send_message(message.chat.id, text="Item 4 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc2Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ойой! 1, чи 2")

@dp.message_handler(state=Loc2Form.Item3_comment)
async def process_loc2_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text="Item 4 => Лінь відповісти - 1 | Залишити коментар - 2.")
    await Loc2Form.next()


# Чек 4 Лок 2
@dp.message_handler(state=Loc2Form.Item4)
async def process_loc2_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc2Form.Item5.set()
        await bot.send_message(message.chat.id, text="Item 5 => Пропустити - арабська один | Залиш коментар - цифра два.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc2Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text="Арабська 1, чи 2 !")

@dp.message_handler(state=Loc2Form.Item4_comment)
async def process_loc2_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text="Item 5 => Пропустити - 1 | Залишити коментар - 2.")
    await Loc2Form.next()


# Чек 5 Лок 2
@dp.message_handler(state=Loc2Form.Item5)
async def process_loc2_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await Loc2Form.Photo.set()
        await bot.send_message(message.chat.id, text="Залиште URL на фото. Пропустити - 1. Залишити - 2")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc2Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text="Промах по клавіатурі detected. 1, чи 2 !")

@dp.message_handler(state=Loc2Form.Item5_comment)
async def process_loc2_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text="Залиште URL на фото, що стосується питання. Ніт - 1. Так - 2")
    await Loc2Form.next()


# Чек 6 (фото) Лок 2
@dp.message_handler(state=Loc2Form.Photo)
async def photo_loc2_url(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(photo_url_reponse='Skip')
        await bot.send_message(message.chat.id, text="Усьо! Обробляємо. Покірно почекайте, будь ласка.")
        await process_checklist_and_send_report(state)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште URL")
        await state.set_state(Loc2Form.Photo_processing)
        await state.update_data(photo_url_reponse=None)
    else:
        await bot.send_message(message.chat.id, text="9, чи 10? Ne chue baba. Повторіть, будь ласка.")

@dp.message_handler(state=Loc2Form.Photo_processing)
async def photo_loc2_url_processing(message: types.Message, state: FSMContext):
    await state.update_data(photo_url_reponse=message.text)

    await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка запиту. Стривайте.")
    await process_checklist_and_send_report(state)


# Чек 1 Лок 3
@dp.message_handler(state=Loc3Form.Item1)
async def process_loc3_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item1_response='Skip')
        await state.set_state(Loc3Form.Item2)
        await bot.send_message(message.chat.id, text="Item 2 => Пропустити - 1  | Залишити коментар - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc3Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ніт, лише цифра 1 чи 2, будь ласка.")

@dp.message_handler(state=Loc3Form.Item1_comment)
async def process_loc3_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text="Item 2 => Пропустити - введіть 1 | Залишити комент - 2.")
    await Loc3Form.next()


# Чек 2 Лок 3
@dp.message_handler(state=Loc3Form.Item2)
async def process_loc3_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc3Form.Item3.set()
        await bot.send_message(message.chat.id, text="Item 3 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc3Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ше раз! 1 чи 2")

@dp.message_handler(state=Loc3Form.Item2_comment)
async def process_loc3_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text="Item 3 => Пропустити - цифра(5 мінус 4) | Залишити комент - цифра(корінь з чотирьох)")
    await Loc3Form.next()


# Чек 3 Лок 3
@dp.message_handler(state=Loc3Form.Item3)
async def process_loc3_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc3Form.Item4.set()
        await bot.send_message(message.chat.id, text="Item 4 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc3Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ойой! 1, чи 2")

@dp.message_handler(state=Loc3Form.Item3_comment)
async def process_loc3_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text="Item 4 => Лінь відповісти - 1 | Залишити коментар - 2.")
    await Loc3Form.next()


# Чек 4 Лок 3
@dp.message_handler(state=Loc3Form.Item4)
async def process_loc3_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc3Form.Item5.set()
        await bot.send_message(message.chat.id, text="Item 5 => Пропустити - арабська один | Залиш коментар - цифра два.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc3Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text="Арабська 1, чи 2 !")

@dp.message_handler(state=Loc3Form.Item4_comment)
async def process_loc3_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text="Item 5 => Пропустити - 1 | Залишити коментар - 2.")
    await Loc3Form.next()


# Чек 5 Лок 3
@dp.message_handler(state=Loc3Form.Item5)
async def process_loc3_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await Loc3Form.Photo.set()
        await bot.send_message(message.chat.id, text="Залиште URL на фото. Пропустити - 1. Залишити - 2")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc3Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text="Промах по клавіатурі detected. 1, чи 2 !")

@dp.message_handler(state=Loc3Form.Item5_comment)
async def process_loc3_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text="Залиште URL на фото, що стосується питання. Ніт - 1. Так - 2")
    await Loc3Form.next()


# Чек 6 (фото) Лок 3
@dp.message_handler(state=Loc3Form.Photo)
async def photo_loc3_url(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(photo_url_reponse='Skip')
        await bot.send_message(message.chat.id, text="Усьо! Обробляємо. Покірно почекайте, будь ласка.")
        await process_checklist_and_send_report(state)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште URL")
        await state.set_state(Loc3Form.Photo_processing)
        await state.update_data(photo_url_reponse=None)
    else:
        await bot.send_message(message.chat.id, text="9, чи 10? Ne chue baba. Повторіть, будь ласка.")

@dp.message_handler(state=Loc3Form.Photo_processing)
async def photo_loc3_url_processing(message: types.Message, state: FSMContext):
    await state.update_data(photo_url_reponse=message.text)

    await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка запиту. Стривайте.")
    await process_checklist_and_send_report(state)


# Чек 1 Лок 4
@dp.message_handler(state=Loc4Form.Item1)
async def process_loc4_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Loc4Form.Item2)
       await bot.send_message(message.chat.id, text="Item 2 => Пропустити - 1  | Залишити коментар - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc4Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ніт, лише цифра 1 чи 2, будь ласка.")

@dp.message_handler(state=Loc4Form.Item1_comment)
async def process_loc4_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text="Item 2 => Пропустити - введіть 1 | Залишити комент - 2.")
    await Loc4Form.next()


# Чек 2 Лок 4
@dp.message_handler(state=Loc4Form.Item2)
async def process_loc4_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc4Form.Item3.set()
        await bot.send_message(message.chat.id, text="Item 3 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc4Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ше раз! 1 чи 2")

@dp.message_handler(state=Loc4Form.Item2_comment)
async def process_loc4_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text="Item 3 => Пропустити - цифра(5 мінус 4) | Залишити комент - цифра(корінь з чотирьох)")
    await Loc4Form.next()


# Чек 3 Лок 4
@dp.message_handler(state=Loc4Form.Item3)
async def process_loc4_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc4Form.Item4.set()
        await bot.send_message(message.chat.id, text="Item 4 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc4Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ойой! 1, чи 2")

@dp.message_handler(state=Loc4Form.Item3_comment)
async def process_loc4_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text="Item 4 => Лінь відповісти - 1 | Залишити коментар - 2.")
    await Loc4Form.next()


# Чек 4 Лок 4
@dp.message_handler(state=Loc4Form.Item4)
async def process_loc4_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc4Form.Item5.set()
        await bot.send_message(message.chat.id, text="Item 5 => Пропустити - арабська один | Залиш коментар - цифра два.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc4Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text="Арабська 1, чи 2 !")

@dp.message_handler(state=Loc4Form.Item4_comment)
async def process_loc4_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text="Item 5 => Пропустити - 1 | Залишити коментар - 2.")
    await Loc4Form.next()


# Чек 5 Лок 4
@dp.message_handler(state=Loc4Form.Item5)
async def process_loc4_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await Loc4Form.Photo.set()
        await bot.send_message(message.chat.id, text="Залиште URL на фото. Пропустити - 1. Залишити - 2")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc4Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text="Промах по клавіатурі detected. 1, чи 2 !")

@dp.message_handler(state=Loc4Form.Item5_comment)
async def process_loc4_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text="Залиште URL на фото, що стосується питання. Ніт - 1. Так - 2")
    await Loc4Form.next()


# Чек 6 (фото) Лок 4
@dp.message_handler(state=Loc4Form.Photo)
async def photo_loc4_url(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(photo_url_reponse='Skip')
        await bot.send_message(message.chat.id, text="Усьо! Обробляємо. Покірно почекайте, будь ласка.")
        await process_checklist_and_send_report(state)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште URL")
        await state.set_state(Loc4Form.Photo_processing)
        await state.update_data(photo_url_reponse=None)
    else:
        await bot.send_message(message.chat.id, text="9, чи 10? Ne chue baba. Повторіть, будь ласка.")

@dp.message_handler(state=Loc4Form.Photo_processing)
async def photo_loc4_url_processing(message: types.Message, state: FSMContext):
    await state.update_data(photo_url_reponse=message.text)

    await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка запиту. Стривайте.")
    await process_checklist_and_send_report(state)


# Чек 1 Лок 5
@dp.message_handler(state=Loc5Form.Item1)
async def process_loc5_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Loc5Form.Item2)
       await bot.send_message(message.chat.id, text="Item 2 => Пропустити - 1  | Залишити коментар - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc5Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ніт, лише цифра 1 чи 2, будь ласка.")

@dp.message_handler(state=Loc5Form.Item1_comment)
async def process_loc5_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text="Item 2 => Пропустити - введіть 1 | Залишити комент - 2.")
    await Loc5Form.next()


# Чек 2 Лок 5
@dp.message_handler(state=Loc5Form.Item2)
async def process_loc5_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc5Form.Item3.set()
        await bot.send_message(message.chat.id, text="Item 3 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc5Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ше раз! 1 чи 2")

@dp.message_handler(state=Loc5Form.Item2_comment)
async def process_loc5_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text="Item 3 => Пропустити - цифра(5 мінус 4) | Залишити комент - цифра(корінь з чотирьох)")
    await Loc5Form.next()


# Чек 3 Лок 5
@dp.message_handler(state=Loc5Form.Item3)
async def process_loc5_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc5Form.Item4.set()
        await bot.send_message(message.chat.id, text="Item 4 => Пропустити - 1 | Залишити - 2.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc5Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ойой! 1, чи 2")

@dp.message_handler(state=Loc5Form.Item3_comment)
async def process_loc5_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text="Item 4 => Лінь відповісти - 1 | Залишити коментар - 2.")
    await Loc5Form.next()


# Чек 4 Лок 5
@dp.message_handler(state=Loc5Form.Item4)
async def process_loc5_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc5Form.Item5.set()
        await bot.send_message(message.chat.id, text="Item 5 => Пропустити - арабська один | Залиш коментар - цифра два.")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc5Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text="Арабська 1, чи 2 !")

@dp.message_handler(state=Loc5Form.Item4_comment)
async def process_loc5_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text="Item 5 => Пропустити - 1 | Залишити коментар - 2.")
    await Loc5Form.next()


# Чек 5 Лок 5
@dp.message_handler(state=Loc5Form.Item5)
async def process_loc5_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await Loc5Form.Photo.set()
        await bot.send_message(message.chat.id, text="Залиште URL на фото. Пропустити - 1. Залишити - 2")
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc5Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text="Промах по клавіатурі detected. 1, чи 2 !")

@dp.message_handler(state=Loc5Form.Item5_comment)
async def process_loc5_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text="Залиште URL на фото, що стосується питання. Ніт - 1. Так - 2")
    await Loc5Form.next()


# Чек 6 (фото) Лок 5     # photo_processing snippets can be made unique for all Locations if needed. If DRY needed. 
@dp.message_handler(state=Loc5Form.Photo)
async def photo_loc5_url(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(photo_url_reponse='Skip')
        await bot.send_message(message.chat.id, text="Усьо! Обробляємо. Покірно почекайте, будь ласка")
        await process_checklist_and_send_report(state)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште URL")
        await state.set_state(Loc5Form.Photo_processing)
        await state.update_data(photo_url_reponse=None)
    else:
        await bot.send_message(message.chat.id, text="9, чи 10? Ne chue baba. Повторіть, будь ласка.")


@dp.message_handler(state=Loc5Form.Photo_processing)
async def photo_loc5_url_processing(message: types.Message, state: FSMContext):
    await state.update_data(photo_url_reponse=message.text)

    await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка запиту. Стривайте.")
    await process_checklist_and_send_report(state)