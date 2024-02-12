import re

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from bot.loader.loader import bot, dp
from bot.keyboards import locations_menu
from bot.handlers.users.photo_url import LeavePhoto
from bot.states.states import ChooseLoc, Loc1Form, Loc2Form, Loc3Form, Loc4Form
from bot.data.text import welcome_text, item1_text, item2_text, item3_text, item4_text, item5_text, num_one_two_text, leave_photo_url_text


# Вітання
@dp.message_handler(Command('start'))
async def welcome(message: types.Message, state: FSMContext) -> None:
    """ command '/start' """
    reply_text = f'{hbold(message.from_user.first_name)}, {welcome_text}'

    await bot.send_message(
        message.chat.id,
        text=reply_text,
        reply_markup=locations_menu.menu
    )
    await ChooseLoc.Location.set()


# Обирай Локацію з locations_kb.menu.
@dp.message_handler(lambda message: bool(re.match("^Location [1-4]$", message.text)), state=ChooseLoc.Location)
async def handle_location(message: types.Message, state: FSMContext):
    location = message.text
    await state.update_data(location=location)
    await bot.send_message(message.chat.id, text=f"{location}. Мерщій заповни чекліст.",
                            reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, text=item1_text)
    if message.text == 'Location 1':
        await state.set_state(Loc1Form.Item1)
    elif message.text == 'Location 2':
        await state.set_state(Loc2Form.Item1)
    elif message.text == 'Location 3':
        await state.set_state(Loc3Form.Item1)
    elif message.text == 'Location 4':
        await state.set_state(Loc4Form.Item1)


# Чек 1 Лок 1
@dp.message_handler(state=Loc1Form.Item1)
async def process_loc1_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Loc1Form.Item2) # або => await Loc1Form.Item2.set()
       await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc1Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc1Form.Item1_comment)
async def process_loc1_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Loc1Form.next()


# Чек 2 Лок 1
@dp.message_handler(state=Loc1Form.Item2)
async def process_loc1_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc1Form.Item3.set()
        await bot.send_message(message.chat.id, text=item3_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc1Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc1Form.Item2_comment)
async def process_loc1_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text=item3_text)
    await Loc1Form.next()


# Чек 3 Лок 1
@dp.message_handler(state=Loc1Form.Item3)
async def process_loc1_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc1Form.Item4.set()
        await bot.send_message(message.chat.id, text=item4_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc1Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc1Form.Item3_comment)
async def process_loc1_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text=item4_text)
    await Loc1Form.next()


# Чек 4 Лок 1
@dp.message_handler(state=Loc1Form.Item4)
async def process_loc1_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc1Form.Item5.set()
        await bot.send_message(message.chat.id, text=item5_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc1Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc1Form.Item4_comment)
async def process_loc1_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text=item5_text)
    await Loc1Form.next()


# Чек 5 Лок 1
@dp.message_handler(state=Loc1Form.Item5)
async def process_loc1_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await state.set_state(LeavePhoto.URL)
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc1Form.Item4_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc1Form.Item5_comment)
async def process_loc1_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text=leave_photo_url_text)
    await state.set_state(LeavePhoto.URL)


# Чек 1 Лок 2
@dp.message_handler(state=Loc2Form.Item1)
async def process_loc2_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Loc2Form.Item2)
       await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc2Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc2Form.Item1_comment)
async def process_loc2_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Loc2Form.next()


# Чек 2 Лок 2
@dp.message_handler(state=Loc2Form.Item2)
async def process_loc2_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc2Form.Item3.set()
        await bot.send_message(message.chat.id, text=item3_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc2Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc2Form.Item2_comment)
async def process_loc2_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text=item3_text)
    await Loc2Form.next()


# Чек 3 Лок 2
@dp.message_handler(state=Loc2Form.Item3)
async def process_loc2_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc2Form.Item4.set()
        await bot.send_message(message.chat.id, text=item4_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc2Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc2Form.Item3_comment)
async def process_loc2_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text=item4_text)
    await Loc2Form.next()


# Чек 4 Лок 2
@dp.message_handler(state=Loc2Form.Item4)
async def process_loc2_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc2Form.Item5.set()
        await bot.send_message(message.chat.id, text=item5_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc2Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc2Form.Item4_comment)
async def process_loc2_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text=item5_text)
    await Loc2Form.next()


# Чек 5 Лок 2
@dp.message_handler(state=Loc2Form.Item5)
async def process_loc2_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await state.set_state(LeavePhoto.URL)
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc2Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc2Form.Item5_comment)
async def process_loc2_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text=leave_photo_url_text)
    await state.set_state(LeavePhoto.URL)


# Чек 1 Лок 3
@dp.message_handler(state=Loc3Form.Item1)
async def process_loc3_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item1_response='Skip')
        await state.set_state(Loc3Form.Item2)
        await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc3Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc3Form.Item1_comment)
async def process_loc3_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Loc3Form.next()


# Чек 2 Лок 3
@dp.message_handler(state=Loc3Form.Item2)
async def process_loc3_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc3Form.Item3.set()
        await bot.send_message(message.chat.id, text=item3_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc3Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc3Form.Item2_comment)
async def process_loc3_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text=item3_text)
    await Loc3Form.next()


# Чек 3 Лок 3
@dp.message_handler(state=Loc3Form.Item3)
async def process_loc3_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc3Form.Item4.set()
        await bot.send_message(message.chat.id, text=item4_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc3Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ойой! 1, чи 2")

@dp.message_handler(state=Loc3Form.Item3_comment)
async def process_loc3_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text=item4_text)
    await Loc3Form.next()


# Чек 4 Лок 3
@dp.message_handler(state=Loc3Form.Item4)
async def process_loc3_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc3Form.Item5.set()
        await bot.send_message(message.chat.id, text=item5_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc3Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc3Form.Item4_comment)
async def process_loc3_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text=item5_text)
    await Loc3Form.next()


# Чек 5 Лок 3
@dp.message_handler(state=Loc3Form.Item5)
async def process_loc3_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await state.set_state(LeavePhoto.URL)
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc3Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc3Form.Item5_comment)
async def process_loc3_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text=leave_photo_url_text)
    await state.set_state(LeavePhoto.URL)


# Чек 1 Лок 4
@dp.message_handler(state=Loc4Form.Item1)
async def process_loc4_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Loc4Form.Item2)
       await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Loc4Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc4Form.Item1_comment)
async def process_loc4_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Loc4Form.next()


# Чек 2 Лок 4
@dp.message_handler(state=Loc4Form.Item2)
async def process_loc4_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Loc4Form.Item3.set()
        await bot.send_message(message.chat.id, text=item3_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Loc4Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc4Form.Item2_comment)
async def process_loc4_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text=item3_text)
    await Loc4Form.next()


# Чек 3 Лок 4
@dp.message_handler(state=Loc4Form.Item3)
async def process_loc4_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Loc4Form.Item4.set()
        await bot.send_message(message.chat.id, text=item4_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Loc4Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc4Form.Item3_comment)
async def process_loc4_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text=item4_text)
    await Loc4Form.next()


# Чек 4 Лок 4
@dp.message_handler(state=Loc4Form.Item4)
async def process_loc4_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Loc4Form.Item5.set()
        await bot.send_message(message.chat.id, text=item5_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Loc4Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc4Form.Item4_comment)
async def process_loc4_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text=item5_text)
    await Loc4Form.next()


# Чек 5 Лок 4
@dp.message_handler(state=Loc4Form.Item5)
async def process_loc4_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await state.set_state(LeavePhoto.URL)
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Loc4Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc4Form.Item5_comment)
async def process_loc4_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text=leave_photo_url_text)
    await state.set_state(LeavePhoto.URL)


# Фото стейт #TODO separate file
# @dp.message_handler(state=LeavePhoto.URL)
# async def photo_url(message: types.Message, state: FSMContext):
#     if message.text == '1':
#         await state.update_data(photo_url_reponse='Skip')
#         await bot.send_message(message.chat.id, text="Усьо! Обробляємо. Покірно почекайте, будь ласка.")
#         await process_checklist_and_send_report(state)
#     elif message.text == '2':
#         await bot.send_message(message.chat.id, text=leave_photo_url_text)
#         await state.set_state(LeavePhoto.URL_processing)
#         await state.update_data(photo_url_reponse=None)
#     else:
#         await bot.send_message(message.chat.id, text=num_one_two_text)

# @dp.message_handler(state=LeavePhoto.URL_processing)
# async def photo_url_processing(message: types.Message, state: FSMContext):
#     await state.update_data(photo_url_reponse=message.text)

#     await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка запиту. Стривайте.")
#     await process_checklist_and_send_report(state)