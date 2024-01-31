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


user_responses = defaultdict(lambda: {"Location": None, "Checklist": [], "Photo": None})


@user_router.message(Command('start'))
async def welcome(message: types.Message) -> None:
    """ Process the command 'start' """
    reply_text = f'{hbold(message.from_user.first_name)}, ласкаво прошу. Почнімо'

    await message.answer(
        text=reply_text,
        reply_markup=locations_kb.menu
    )


@user_router.message(F.text == 'Location 1') # equals lambda message: message.text == 'Location 1'
async def choose_location(message: types.Message):
    location = message.text
    user_id = message.from_user.id

    if user_id not in user_responses:
        user_responses[user_id] = {"Location": None, "Checklist": [], "Photo": None}

    user_responses[user_id]["Location"] = location
    # чекліст
    checklist = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
    user_responses[user_id]["Checklist"] = checklist

    await message.answer(f"Обрано {location}. Заповнимо чекліст.\n \
                         Введи 1 - Залишити чистим | 2 - Залишити коментар.")
    await message.answer(f"Щодо {checklist[0]}, який твій вибір?")


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


@user_router.message(lambda message: user_responses[message.from_user.id].get("CommentState", False))
async def handle_checklist_comment(message: types.Message):
    user_id = message.from_user.id

    if user_responses[user_id]["Checklist"]:
        current_checklist_item = user_responses[user_id]["Checklist"][0]
        current_checklist_item["Response"] = message.text
        user_responses[user_id].pop("CommentState", None)
        # Перевіряв, чи доєднались дані до user_responses
        print(user_responses)
        await continue_checklist(user_id)
    else:
        print("Checklist is done, handle accordingly")

''' 
    TODO https://docs.aiogram.dev/uk-ua/latest/dispatcher/finite_state_machine/index.html  
    user_responses - треш. Краще розібратися з FSM, та інтегрувати цю логіку
'''


@user_router.message(lambda message: user_responses[message.from_user.id].get("Checklist"))
async def continue_checklist(message: types.Message):
    user_id = message.from_user.id

    if user_responses[user_id]["Checklist"]:
        next_item = user_responses[user_id]["Checklist"][0]
        await bot.send_message(user_id, f"Щодо {next_item}, який вибір?")
    else:
        print("Checklist completed:", user_responses[user_id])
        await bot.send_message(user_id, "Бажаєте загрузити фото? Введіть 1 - пропустити, 2 - завантажити")


@user_router.message(lambda message: message.text in ["Upload a photo", "Skip photo"])
async def handle_photo_upload(message: types.Message):
    user_id = message.from_user.id
    if message.text == '1':
        await bot.send_message(user_id, "Загрузіть фото, що стосується чеклісту.")
    else: 
        pass


def generate_report(user_response):
    location = user_response['Location']
    checklist_items = "\n".join([f"{item['Item']}: {item['Response']}" for item in user_response["Checklist"]])
    photo = user_response['Photo']

    report = f"Location: {location}\n\nChecklist:\n{checklist_items}\n\n"
    report += f"Photo: {photo}\n"

    return report


@user_router.message(generate_report)
async def send_to_chatgpt(message: types.Message):
    user_id = message.from_user.id
    user_responses[user_id]["Photo"] = message.photo[-1].file_id

    report = generate_report(user_responses[user_id])
    try:
        openai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=report,
            max_tokens=200
        )
        analyzed_report = openai_response.choices[0].text.strip()
        # Назад юзеру
        await bot.send_message(user_id, f"Analysis Result:\n{analyzed_report}", parse_mode=types.ParseMode.MARKDOWN)

    except Exception as e:
        logging.error(f"Error in OpenAI analysis: {e}")
        await bot.send_message(user_id, "Error in OpenAI analysis. Please try again later.")