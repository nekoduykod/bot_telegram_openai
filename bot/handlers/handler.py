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
    Location = State()  # Will be represented in storage as 'DialogueStates:Location'
    Checklist = State()  # Will be represented in storage as 'DialogueStates:Checklist'
    WaitingForChoice = State()

class ChecklistForm(StatesGroup):
    Item1 = State()
    Item2 = State()
    Item3 = State()
    Item4 = State()
    Item5 = State()


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
    choice = message.text

    if choice == '1':
        # go to next item
        await ChecklistForm.next()
    elif choice == '2':
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 1")
        await ChecklistForm.next()

@dp.message_handler(state=ChecklistForm.Item2)
async def process_item2(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text="Item 2, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    choice = message.text

    if choice == '1':
        # User chose to skip, move to the next item
        await ChecklistForm.next()
    elif choice == '2':
        # User chose to leave a comment, ask for comment
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 2")
        await ChecklistForm.next()


@dp.message_handler(state=ChecklistForm.Item3)
async def process_item3(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text="Item 3, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    choice = message.text

    if choice == '1':
        # User chose to skip, move to the next item
        await ChecklistForm.next()
    elif choice == '2':
        # User chose to leave a comment, ask for comment
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 3")
        await ChecklistForm.next()


@dp.message_handler(state=ChecklistForm.Item4)
async def process_item4(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text="Item 4, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    choice = message.text

    if choice == '1':
        # User chose to skip, move to the next item
        await ChecklistForm.next()
    elif choice == '2':
        # User chose to leave a comment, ask for comment
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 4")
        await ChecklistForm.next()


@dp.message_handler(state=ChecklistForm.Item5)
async def process_item5(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text="Item 5, введіть цифру 1 - Пропустити | 2 - Залишити коментар.")
    choice = message.text

    if choice == '1':
        # User chose to skip, finish the checklist
        await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка результатів...")
        await process_checklist_and_send_report(state)
        await state.finish()
    elif choice == '2':
        # User chose to leave a comment, ask for comment
        await bot.send_message(message.chat.id, text="Залиште коментар для Item 5:")
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
    print(checklist_responses); print(location)
    # Process the checklist data and send the report to OpenAI
    # ...

    # Send a completion message to the user

    # Reset the state
    await bot.send_message(state.user, text="Чекліст завершено. Дякуємо!")
    await state.finish()


# @dp.message_handler(state='*')
# async def process_checklist(message: types.Message, state: FSMContext):
#     user_choice = message.text
#     if user_choice == '2':
#         await bot.send_message(message.chat.id, text = f"Будь ласка, залиши коментар.")
#         user_input = message.text
#         checklist = await state.get_data()
#         for item in checklist['checklist']:
#             if item['Item'] == checklist['location']:
#                 item["Response"] = user_input
#                 break
#     await state.finish()


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

 
# @dp.message.message(lambda message: message.text in ['1', '2']) # (F.text.in_(['1', '2']))
# async def handle_checklist_item(message: types.Message):
#     user_id = message.from_user.id
#     current_checklist_item = user_responses[user_id]["Checklist"].pop(0)
#     current_checklist_item["Response"] = message.text
#     if message.text == '1':
#         user_responses[user_id]["CommentState"] = False
#         await continue_checklist(user_id)
#     else:
#         user_responses[user_id]["CommentState"] = True
#         await message.answer(f"Будь ласка, залиши коментар {current_checklist_item['Item']}.")

# ### !!!
# @dp.message.message(lambda message: user_responses[message.from_user.id].get("CommentState", False))
# async def handle_checklist_comment(message: types.Message):
#     user_id = message.from_user.id
#     # Get the current checklist item
#     current_checklist_item = user_responses[user_id]["Checklist"][0]
#     # Set the comment for the current checklist item
#     current_checklist_item["Response"] = message.text
#     # Remove the CommentState flag
#     user_responses[user_id].pop("CommentState", None)
#     print(user_responses)
#     await continue_checklist(user_id)


# async def continue_checklist(user_id):
#     if user_responses[user_id]["Checklist"]:
#         next_item = user_responses[user_id]["Checklist"][0]
#         await bot.send_message(user_id, f"Щодо {next_item['Item']}, який вибір?")
#     else:
#         # Якщо чекліст пройдений, попроси загальний комент
#         await bot.send_message(user_id, "Бажаєте загрузити фото? Введіть 1 - пропустити, 2 - завантажу")


# @dp.message.message(lambda message: message.text in ["Upload a photo", "Skip photo"])
# async def handle_photo_upload(message: types.Message):
#     user_id = message.from_user.id
#     if message.text == '1':
#         await bot.send_message(user_id, "Загрузіть фото, що стосується чеклісту.")
#     else: 
#         pass


# def generate_report(user_response):
#     location = user_response['Location']
#     checklist_items = "\n".join([f"{item['Item']}: {item['Response']}" for item in user_response["Checklist"]])
#     photo = user_response['Photo']

#     report = f"Location: {location}\n\nChecklist:\n{checklist_items}\n\n"
#     report += f"Photo: {photo}\n"

#     return report


# @dp.message(generate_report)
# async def send_to_chatgpt(message: types.Message):
#     user_id = message.from_user.id
#     user_responses[user_id]["Photo"] = message.photo[-1].file_id

#     report = generate_report(user_responses[user_id])
#     try:

#         openai_response = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt=report,
#             max_tokens=200
#         )
#         analyzed_report = openai_response.choices[0].text.strip()
#         # Send the analyzed report to the user
#         await bot.send_message(user_id, f"Analysis Result:\n{analyzed_report}", parse_mode=types.ParseMode.MARKDOWN)

#     except Exception as e:
#         logging.error(f"Error in OpenAI analysis: {e}")
#         await bot.send_message(user_id, "Error in OpenAI analysis. Please try again later.")