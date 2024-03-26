from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton


def get_week_menu_kb(menu):
    ikb = InlineKeyboardMarkup(row_width=2)
    # if there is some data in menu - show it, else - just show default buttons
    if menu:
        for index, day in enumerate(menu):
            button = InlineKeyboardButton(text='День' + str(index+1), callback_data=f'0')
            ikb.add(button)
            # button for each dish
            for dish in day.get('dishes'):
                button = InlineKeyboardButton(text=dish.get('title'), callback_data=f"dish_id_{dish.get('id')}")
                ikb.add(button)
            button = InlineKeyboardButton(text='_____________', callback_data='0')
            ikb.add(button)
    button = InlineKeyboardButton(text='Добавить', callback_data='add_day')
    ikb.add(button)
    reset_button = InlineKeyboardButton(text='Сбросить меню', callback_data='reset_menu')
    ingredients_button = InlineKeyboardButton(text='Список ингридиентов', callback_data='get_ingredients_list')
    ikb.add(reset_button, ingredients_button)
    return ikb


def get_dish_kb(dish_id):
    ikb = InlineKeyboardMarkup(row_width=3)
    buttons = []

    button = InlineKeyboardButton(text='<<', callback_data=f'previous_dish_{dish_id}')
    buttons.append(button)

    button = InlineKeyboardButton(text='OK', callback_data=f'menu')
    buttons.append(button)

    button = InlineKeyboardButton(text='>>', callback_data=f'next_dish_{dish_id}')
    buttons.append(button)

    ikb.add(*buttons)
    return ikb


def delete_message_button():
    ikb = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='Закрыть', callback_data='delete_message')
    ikb.add(button)
    return ikb