import re

from aiogram import types
# from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from main import bot, dp
from bot.keyboards.inline import keyboards_menu
from bot.handlers.users.photo_url_handler import LeavePhoto
from bot.states.states import ChooseButton, Issue1Form, Issue2Form, Issue3Form, Issue4Form
from bot.data.text import item1_text, item2_text, item3_text, item4_text, item5_text, num_one_two_text, leave_photo_url_text


@dp.message_handler(commands=["locations"])
async def choose_loc(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Оберіть питання, що турбує.',
                           reply_markup=keyboards_menu.inline_kb)
    await ChooseButton.Issues.set()


@dp.callback_query_handler(lambda query: re.match('^Issue[1-4]$', query.data), state=ChooseButton.Issues)
async def loc_answer_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'Issue1':
        location = call.data
        await state.update_data(location=location)
        await bot.send_message(chat_id=call.message.chat.id, text=item1_text)
        await call.answer(text='Issue 1 обрано')
        await Issue1Form.Item1.set()

    elif call.data == 'Issue2':
        location = call.data
        await state.update_data(location=location)
        await bot.send_message(chat_id=call.message.chat.id, text=item1_text)
        await call.answer(text='Issue 2 обрано')
        await Issue2Form.Item1.set()

    elif call.data == 'Issue3':
        location = call.data
        await state.update_data(location=location)
        await bot.send_message(chat_id=call.message.chat.id, text=item1_text)
        await call.answer(text='Issue 3 обрано')
        await Issue3Form.Item1.set()

    elif call.data == 'Issue4':
        location = call.data
        await state.update_data(location=location)
        await bot.send_message(chat_id=call.message.chat.id, text=item1_text)
        await call.answer(text='Issue 4 обрано')
        await Issue4Form.Item1.set()


# Чек 1 Лок 1
@dp.message_handler(state=Issue1Form.Item1)
async def process_issue1_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item1_response='Skip')
        await state.set_state(Issue1Form.Item2)
        await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Issue1Form.Item2)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue1Form.Item1_comment)
async def process_issue1_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Issue1Form.Item2.set()


# Чек 2 Лок 1
@dp.message_handler(state=Issue1Form.Item2)
async def process_issue1_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Issue1Form.Item3.set()
        await bot.send_message(message.chat.id, text=item3_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Issue1Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue1Form.Item2_comment)
async def process_issue1_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text=item3_text)
    await Issue1Form.next()


# Чек 3 Лок 1
@dp.message_handler(state=Issue1Form.Item3)
async def process_issue1_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Issue1Form.Item4.set()
        await bot.send_message(message.chat.id, text=item4_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Issue1Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue1Form.Item3_comment)
async def process_issue1_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text=item4_text)
    await Issue1Form.next()


# Чек 4 Лок 1
@dp.message_handler(state=Issue1Form.Item4)
async def process_issue1_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Issue1Form.Item5.set()
        await bot.send_message(message.chat.id, text=item5_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Issue1Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue1Form.Item4_comment)
async def process_issue1_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text=item5_text)
    await Issue1Form.next()


# Чек 5 Лок 1
@dp.message_handler(state=Issue1Form.Item5)
async def process_issue1_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await state.set_state(LeavePhoto.URL)
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Issue1Form.Item4_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue1Form.Item5_comment)
async def process_issue1_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text=leave_photo_url_text)
    await state.set_state(LeavePhoto.URL)


# Чек 1 Лок 2
@dp.message_handler(state=Issue2Form.Item1)
async def process_issue2_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Issue2Form.Item2)
       await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Issue2Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue2Form.Item1_comment)
async def process_issue2_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Issue2Form.next()


# Чек 2 Лок 2
@dp.message_handler(state=Issue2Form.Item2)
async def process_issue2_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Issue2Form.Item3.set()
        await bot.send_message(message.chat.id, text=item3_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Issue2Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue2Form.Item2_comment)
async def process_issue2_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text=item3_text)
    await Issue2Form.next()


# Чек 3 Лок 2
@dp.message_handler(state=Issue2Form.Item3)
async def process_issue2_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Issue2Form.Item4.set()
        await bot.send_message(message.chat.id, text=item4_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Issue2Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue2Form.Item3_comment)
async def process_issue2_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text=item4_text)
    await Issue2Form.next()


# Чек 4 Лок 2
@dp.message_handler(state=Issue2Form.Item4)
async def process_issue2_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Issue2Form.Item5.set()
        await bot.send_message(message.chat.id, text=item5_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Issue2Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue2Form.Item4_comment)
async def process_issue2_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text=item5_text)
    await Issue2Form.next()


# Чек 5 Лок 2
@dp.message_handler(state=Issue2Form.Item5)
async def process_issue2_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await state.set_state(LeavePhoto.URL)
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Issue2Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue2Form.Item5_comment)
async def process_issue2_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text=leave_photo_url_text)
    await state.set_state(LeavePhoto.URL)


# Чек 1 Лок 3
@dp.message_handler(state=Issue3Form.Item1)
async def process_issue3_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item1_response='Skip')
        await state.set_state(Issue3Form.Item2)
        await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Issue3Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue3Form.Item1_comment)
async def process_issue3_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Issue3Form.next()


# Чек 2 Лок 3
@dp.message_handler(state=Issue3Form.Item2)
async def process_issue3_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Issue3Form.Item3.set()
        await bot.send_message(message.chat.id, text=item3_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Issue3Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue3Form.Item2_comment)
async def process_issue3_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text=item3_text)
    await Issue3Form.next()


# Чек 3 Лок 3
@dp.message_handler(state=Issue3Form.Item3)
async def process_issue3_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Issue3Form.Item4.set()
        await bot.send_message(message.chat.id, text=item4_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Issue3Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text="Ойой! 1, чи 2")

@dp.message_handler(state=Issue3Form.Item3_comment)
async def process_issue3_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text=item4_text)
    await Issue3Form.next()


# Чек 4 Лок 3
@dp.message_handler(state=Issue3Form.Item4)
async def process_issue3_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Issue3Form.Item5.set()
        await bot.send_message(message.chat.id, text=item5_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Issue3Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue3Form.Item4_comment)
async def process_issue3_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text=item5_text)
    await Issue3Form.next()


# Чек 5 Лок 3
@dp.message_handler(state=Issue3Form.Item5)
async def process_issue3_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await state.set_state(LeavePhoto.URL)
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Issue3Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue3Form.Item5_comment)
async def process_issue3_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text=leave_photo_url_text)
    await state.set_state(LeavePhoto.URL)


# Чек 1 Лок 4
@dp.message_handler(state=Issue4Form.Item1)
async def process_issue4_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
       await state.update_data(item1_response='Skip')
       await state.set_state(Issue4Form.Item2)
       await bot.send_message(message.chat.id, text=item2_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 1:")
        await state.set_state(Issue4Form.Item1_comment)
        await state.update_data(item1_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue4Form.Item1_comment)
async def process_issue4_item1_comment(message: types.Message, state: FSMContext):
    await state.update_data(item1_response=message.text)

    await bot.send_message(message.chat.id, text=item2_text)
    await Issue4Form.next()


# Чек 2 Лок 4
@dp.message_handler(state=Issue4Form.Item2)
async def process_issue4_item2(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item2_response='Skip')
        await Issue4Form.Item3.set()
        await bot.send_message(message.chat.id, text=item3_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 2:")
        await state.set_state(Issue4Form.Item2_comment)
        await state.update_data(item2_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue4Form.Item2_comment)
async def process_issue4_item2_comment(message: types.Message, state: FSMContext):
    await state.update_data(item2_response=message.text)

    await bot.send_message(message.chat.id, text=item3_text)
    await Issue4Form.next()


# Чек 3 Лок 4
@dp.message_handler(state=Issue4Form.Item3)
async def process_issue4_item3(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item3_response='Skip')
        await Issue4Form.Item4.set()
        await bot.send_message(message.chat.id, text=item4_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 3:")
        await state.set_state(Issue4Form.Item3_comment)
        await state.update_data(item3_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue4Form.Item3_comment)
async def process_issue4_item3_comment(message: types.Message, state: FSMContext):
    await state.update_data(item3_response=message.text)

    await bot.send_message(message.chat.id, text=item4_text)
    await Issue4Form.next()


# Чек 4 Лок 4
@dp.message_handler(state=Issue4Form.Item4)
async def process_issue4_item4(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item4_response='Skip')
        await Issue4Form.Item5.set()
        await bot.send_message(message.chat.id, text=item5_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 4:")
        await state.set_state(Issue4Form.Item4_comment)
        await state.update_data(item4_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue4Form.Item4_comment)
async def process_issue4_item4_comment(message: types.Message, state: FSMContext):
    await state.update_data(item4_response=message.text)

    await bot.send_message(message.chat.id, text=item5_text)
    await Issue4Form.next()


# Чек 5 Лок 4
@dp.message_handler(state=Issue4Form.Item5)
async def process_issue4_item5(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(item5_response='Skip')
        await state.set_state(LeavePhoto.URL)
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Коментар для Item 5:")
        await state.set_state(Issue4Form.Item5_comment)
        await state.update_data(item5_response=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=Issue4Form.Item5_comment)
async def process_issue4_item5_comment(message: types.Message, state: FSMContext):
    await state.update_data(item5_response=message.text)

    await bot.send_message(message.chat.id, text=leave_photo_url_text)
    await state.set_state(LeavePhoto.URL)