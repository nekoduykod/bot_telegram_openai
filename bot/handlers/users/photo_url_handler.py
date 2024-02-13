from aiogram import types
from loader import bot, dp
from aiogram.dispatcher import FSMContext

from bot.functions.request_chatgpt import process_checklist_and_send_report
from bot.states.states import LeavePhoto
from bot.data.text import num_one_two_text, leave_photo_url_text


@dp.message_handler(state=LeavePhoto.URL)
async def leave_photo_url(message: types.Message, state: FSMContext):
    if message.text == '1':
        await state.update_data(photo_url_reponse='Skip')
        await bot.send_message(message.chat.id, text="Усьо! Обробляємо. Покірно почекайте.")
        await process_checklist_and_send_report(state)
    elif message.text == '2':
        await bot.send_message(message.chat.id, text=leave_photo_url_text)
        await state.set_state(LeavePhoto.URL_processing)
        await state.update_data(photo_url_reponse=None)
    else:
        await bot.send_message(message.chat.id, text=num_one_two_text)

@dp.message_handler(state=LeavePhoto.URL_processing)
async def photo_url_processing(message: types.Message, state: FSMContext):
    await state.update_data(photo_url_reponse=message.text)

    await bot.send_message(message.chat.id, text="Чекліст завершено. Обробка запиту. Стривайте.")
    await process_checklist_and_send_report(state)