from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import bot
from logger import log
import json


async def send_error_msg(chat_id):
    log.info('send_error_msg')
    await bot.send_message(text=f'<b>Ошибка, попробуйте позже</b>',
                           chat_id=chat_id, parse_mode='HTML')


async def reset_state(state: FSMContext):
    # Cancel state if it exists
    current_state = await state.get_state()
    if current_state:
        await state.finish()


def convert_json_to_dict(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        print()
        return json.load(file)
