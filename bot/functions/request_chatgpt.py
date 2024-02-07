import logging
import json
import openai

from bot_instance import bot
from aiogram.dispatcher import FSMContext

from token_api import OPENAI_API_KEY


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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
        # TODO loggin print data if needed
        data_string = json.dumps(data)

        prompt_text = "Analyze the following questions/data:"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt_text + data_string,
            max_tokens=1000
        )

        chatgpt_response = response.choices[0].text.strip()

        await bot.send_message(state.user, text=chatgpt_response)
        await bot.send_message(state.user, text="Дякую. Сонячного дня! Звертайтесь.")

        await state.finish()

    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API Error: {e}")
        await bot.send_message(state.user, text="Халепа. Перепрошую. Над проблемою працюють, зверніться пізніше.")

    except Exception as e:
        logging.exception(f"Unexpected Error: {e}")
        await bot.send_message(state.user, text="Йой! Технічні проблеми. Буль ласка, зверніться пізніше.")