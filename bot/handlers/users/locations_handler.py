import re

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import bot, dp
from bot.keyboards.inline import keyboards_menu
from bot.handlers.users.photo_url_handler import LeavePhoto
from bot.states.states import ChooseLoc, Loc1Form, Loc2Form, Loc3Form, Loc4Form
from bot.data.text import item1_text, item2_text, item3_text, item4_text, item5_text, num_one_two_text, leave_photo_url_text


# Обирай Локацію з locations_kb.menu.
@dp.callback_query_handler(lambda query: re.match('^Loc[1-4]$', query.data), state="*")
async def handle_location_callback(call: CallbackQuery, state: FSMContext):
    location = call.data
    await state.update_data(location=location)
    # await bot.send_message(call.message.chat.id, text=f"Location {location}. Мерщій заповни чекліст. 1 - пропустити. 2 - Залишити коментар.", 
    #                                         reply_markup=keyboards_menu.menu)
    # await bot.send_message(call.message.chat.id, text=item1_text)
    if call.data == 'Loc1':
        await Loc1Form.Item1.set()
    elif call.data == 'Loc2':
        await Loc2Form.Item1.set()
    elif call.data == 'Loc3':
        await Loc3Form.Item1.set()
    elif call.data == 'Loc4':
        await Loc4Form.Item1.set()

# found example but still not working 
# dp.register_callback_query_handler(process_gender_search, lambda query: query.data in ('1', '0'), state=Search.gender)
# async def process_gender_search(query: types.CallbackQuery, state: FSMContext):
#     await state.update_data(gender=query.data)
#     await Search.next()
#     await query.message.edit_text(hbold(' :'), reply_markup=city_search_kb(), parse_mode=ParseMode.HTML)


# Чек 1 Лок 1
@dp.message_handler(state=Loc1Form.Item1)
async def process_loc1_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await Loc1Form.Item2.set()
       await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await Loc1Form.Item2.set()
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Loc1Form.Item1_comment)
async def process_loc1_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Loc1Form.Item2.set()


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