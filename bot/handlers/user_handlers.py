import logging
from collections import defaultdict

from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.utils.markdown import hbold
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot_instance import bot
from bot.keyboards import locations_kb
import openai


logging.basicConfig(level=logging.INFO)


user_router = Router()


user_responses = defaultdict(lambda: {"Location": None, "Checklist": [], "General Comment": None, "Photo": None})


@user_router.message(Command('start'))
async def welcome(msg: types.Message) -> None:
    """ Process the command 'start' """
    reply_text = f'{hbold(msg.from_user.first_name)}, ласкаво прошу. Почнімо'

    await msg.answer(
        text=reply_text,
        # reply_markup=locations_kb.menu
    )


@user_router.message(Command('location'))
async def keyboard_handler(message: types.Message) -> None:
    await message.answer(f'Обери локацію!') # reply_markup=locations_kb.menu


@user_router.message(F.text == 'Location 1') # equals lambda message: message.text == 'Location 1'
async def choose_location(message: types.Message):
    location = message.text
    
    user_id = message.from_user.id
    if user_id not in user_responses:
        user_responses[user_id] = {"Location": None, "Checklist": [], "General Comment": None, "Photo": None}

    user_responses[user_id]["Location"] = location
    await message.answer(f"Обрано {location}. Заповнимо чекліст.\n \
                         Введи 1 - Залишити чистим | 2 - Залишити коментар.")

    # Present the checklist
    checklist = [{"Item": item, "Response": None} for item in ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]]
    user_responses[user_id]["Checklist"] = checklist

    # for item in checklist:
    await message.answer(f"Щодо {checklist[0]['Item']}, який твій вибір?")


@user_router.message(lambda message: message.text in ['1', '2']) # (F.text.in_(['1', '2']))
async def handle_checklist_item(message: types.Message):
    user_id = message.from_user.id
    current_checklist_item = user_responses[user_id]["Checklist"].pop(0)
    current_checklist_item["Response"] = message.text
    if message.text == '1':
        user_responses[user_id]["CommentState"] = False
        await continue_checklist(user_id)
    else:
        user_responses[user_id]["CommentState"] = True
        await message.answer(f"Будь ласка, залиши коментар {current_checklist_item['Item']}.")
        await message.answer("Відправ цифру: Залишити чистим - 1 | Залишити коментар - 2")
        await message.answer(f"Щодо {current_checklist_item['Item']}, який твій вибір?")
        # TODO writing text to the Item, memorizing it to the database user_responses
        

async def continue_checklist(user_id):
    if user_responses[user_id]["Checklist"]:
        next_item = user_responses[user_id]["Checklist"][0]
        await bot.send_message(user_id, f"Щодо {next_item['Item']}, який вибір?")
    else:
        # Якщо чекліст пройдений, попроси загальний комент
        await bot.send_message(user_id, "Майже все. Залиши загальне повідомлення.")
        user_responses[user_id]["General Comment"] = None
        # Чи треба фото
        await bot.send_message(user_id, "Бажаєте загрузити фото? Введіть 1 - пропустити, 2 - завантажу")


@user_router.message(lambda message: message.text in ["Upload a photo", "Skip photo"])
async def handle_photo_upload(message: types.Message):
    user_id = message.from_user.id
    if message.text == '1':
        await bot.send_message(user_id, "Загрузіть фото, що стосується чеклісту.")
    else: 
        pass


@user_router.message(lambda message: True)
async def handle_general_comment(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_responses and user_responses[user_id].get("CommentState", False):
        user_responses[user_id]["General Comment"] = message.text
        user_responses[user_id].pop("CommentState", None)
    else:
        pass


def generate_report(user_response):
    location = user_response['Location']
    checklist_items = "\n".join([f"{item['Item']}: {item['Response']}" for item in user_response["Checklist"]])
    general_comment = user_response['General Comment']
    photo = user_response['Photo']

    report = f"Location: {location}\n\nChecklist:\n{checklist_items}\n\n"
    report += f"General Comment: {general_comment}\n"
    report += f"Photo: {photo}\n"

    return report


@user_router.message(generate_report)
async def send_to_chatgpt(message: types.Message):
    user_id = message.from_user.id
    user_responses[user_id]["Photo"] = message.photo[-1].file_id
    # Generate report
    report = generate_report(user_responses[user_id])
    try:
        # Send the report to OpenAI for analysis
        openai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=report,
            max_tokens=200
        )
        analyzed_report = openai_response.choices[0].text.strip()
        # Send the analyzed report to the user
        await bot.send_message(user_id, f"Analysis Result:\n{analyzed_report}", parse_mode=types.ParseMode.MARKDOWN)

    except Exception as e:
        logging.error(f"Error in OpenAI analysis: {e}")
        await bot.send_message(user_id, "Error in OpenAI analysis. Please try again later.")