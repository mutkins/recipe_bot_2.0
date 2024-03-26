from aiogram import Dispatcher
from handlers.user.user_menu import *
from handlers.user.utils import *


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, state='*', commands=['start', 'старт'])
    # dp.register_message_handler(send_recipe, state='*', commands=['get'])
    dp.register_message_handler(get_week_menu, commands=['menu'])
    dp.register_callback_query_handler(get_week_menu, text='menu')
    dp.register_callback_query_handler(add_day, text='add_day')
    # dp.register_callback_query_handler(open_day, lambda callback: callback.data.startswith('day_'))
    # dp.register_callback_query_handler(change_dish, lambda callback: callback.data.startswith('changeDish'))
    dp.register_callback_query_handler(next_dish, lambda callback: callback.data.startswith('next_dish'))
    dp.register_callback_query_handler(previous_dish, lambda callback: callback.data.startswith('previous_dish'))
    dp.register_callback_query_handler(open_dish, lambda callback: callback.data.startswith('dish_id'))
    dp.register_callback_query_handler(reset_menu, text='reset_menu')
    dp.register_callback_query_handler(get_ingredients_list, text='get_ingredients_list')
    dp.register_callback_query_handler(plug, text='0')
    dp.register_callback_query_handler(delete_message, text='delete_message')


