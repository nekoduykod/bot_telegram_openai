from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold

from bot_instance import bot
from bot.keyboards import locations_kb


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class DialogueStates(StatesGroup):
    Location = State()  # represented in storage DialogueStates:Location'
    Checklist = State()  #  as 'DialogueStates:Checklist'
    WaitingForChoice = State()

class ChecklistForm(StatesGroup):
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


@dp.message_handler(Command('start'))
async def welcome(message: types.Message, state: FSMContext) -> None:
    """ The command 'start' """
    reply_text = f'{hbold(message.from_user.first_name)}, ласкаво прошу. Почнімо. Оберіть локацію, що вас цікавить, будь ласка.'

    await bot.send_message(
        message.chat.id,
        text=reply_text,
        reply_markup=locations_kb.menu
    )
    await DialogueStates.Location.set()


@dp.message_handler(lambda message: message.text == 'Location 1', state=DialogueStates.Location)
async def choose_location(message: types.Message, state: FSMContext):
    location = message.text
    await state.update_data(location=location)

    await bot.send_message(message.chat.id, text=f"{location}. Заповніть, будь ласка, чекліст")

    await bot.send_message(message.chat.id, text="Item 1, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    await ChecklistForm.Item1.set()


@dp.message_handler(state=ChecklistForm.Item1)
async def process_item1(message: types.Message, state: FSMContext):
    if message.text == '1':
        # Go to the next item
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 1")
        # Set the state to collect comments for Item 1
        await state.set_state(ChecklistForm.Item1_comment)
        await state.update_data(item1_response=None)

@dp.message_handler(state=ChecklistForm.Item1_comment)
async def process_item1_comment(message: types.Message, state: FSMContext):
    # Collect the comment for Item 1
    await state.update_data(item1_response=message.text)
    await bot.send_message(message.chat.id, text="Item 2, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    await ChecklistForm.Item2.set()


@dp.message_handler(state=ChecklistForm.Item2)
async def process_item2(message: types.Message, state: FSMContext):

    if message.text == '1':
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 2")
        user_comment = message.text
        await state.update_data(item2_response=user_comment)
        await bot.send_message(message.chat.id, text="Item 3, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
        await ChecklistForm.next()


@dp.message_handler(state=ChecklistForm.Item3)
async def process_item3(message: types.Message, state: FSMContext):

    if message.text == '1':
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 3")
        user_comment = message.text
        await state.update_data(item3_response=user_comment)
        await bot.send_message(message.chat.id, text="Item 4, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
        await ChecklistForm.next()


@dp.message_handler(state=ChecklistForm.Item4)
async def process_item4(message: types.Message, state: FSMContext):

    if message.text == '1':
        await ChecklistForm.next()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 4")
        user_comment = message.text
        await state.update_data(item4_response=user_comment)
        await bot.send_message(message.chat.id, text="Item 5, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
        await ChecklistForm.next()


@dp.message_handler(state=ChecklistForm.Item5)
async def process_item5(message: types.Message, state: FSMContext):

    if message.text == '1':
        await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка результатів...")
        await process_checklist_and_send_report(state)
        await state.finish()
    elif message.text == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 5:")
        user_comment = message.text
        await state.update_data(item5_response=user_comment)
        await process_checklist_and_send_report(state)


async def process_checklist_and_send_report(state: FSMContext):
    data = await state.get_data()
    location = data.get('location')
    checklist_responses = [
        data.get('item1_response'),
        data.get('item2_response'),
        data.get('item3_response'),
        data.get('item4_response'),
        data.get('item5_response'),
    ]
    print(checklist_responses); print(location); print(data)
     
    # ... TODO

    # Reset the state
    await bot.send_message(state.user, text="Чекліст завершено. Дякуємо!")
    await state.finish()


""" example of a possible solution of wrong data written """
# @dp.message_handler(state=ChecklistForm.Item1)
# async def process_item1(message: types.Message, state: FSMContext):
#     if message.text == '1':
#         # Go to the next item
#         await ChecklistForm.next()
#     elif message.text == '2':
#         await bot.send_message(message.chat.id, text="Залиште коментар для Item 1")
#         # Set the state to collect comments for Item 1
#         await state.set_state(ChecklistForm.Item1_comment)
#         await state.update_data(item1_response=None)

# @dp.message_handler(state=ChecklistForm.Item1_comment)
# async def process_item1_comment(message: types.Message, state: FSMContext):
#     # Collect the comment for Item 1
#     await state.update_data(item1_response=message.text)
#     await state.set_state(ChecklistForm.next())


""" my past efforts with for loop. In vain... """
    # for item in checklist:
    #     await message.answer(f"{item['Item']}, введіть цифру 1 | 2:")
    #     user_choice = message.text
    #     if user_choice == '2':
    #         await message.answer(f"Будь ласка, залиши коментар.")
    #         user_input = message.text
    #         item["Response"] = user_input
    #     else:
    #         pass

    # print(user_responses)


              #  test
# @dp.message_handler(state=ChecklistForm.Item2)
# async def process_item2(message: types.Message, state: FSMContext):
#     await bot.send_message(message.chat.id, text="Item 2, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")

#     if message.text == '1':
#         await ChecklistForm.next()
#     elif message.text == '2':
#         await bot.send_message(message.chat.id, text="Залиште коментар для Item 2")
#         await state.set_state(ChecklistForm.Item2_comment)
#         await state.update_data(item2_response=None)  # Initialize response

# @dp.message_handler(state=ChecklistForm.Item2_comment)
# async def process_item2_comment(message: types.Message, state: FSMContext):
#     # Collect the comment for Item 2
#     await state.update_data(item2_response=message.text)
#     await state.set_state(ChecklistForm.next())  # Now move to the next state