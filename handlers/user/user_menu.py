from logger import log
from aiogram.utils.exceptions import MessageNotModified, MessageTextIsEmpty
from .utils import *
from aiogram.dispatcher import FSMContext
from keyboards.keyboards import *
from tools import *


async def send_welcome(message: types.Message, state: FSMContext):
    try:
        # Reset state if it exists
        await reset_state(state=state)
        await message.answer("<b>Книга рецептов поможет собрать меню на несколько дней</b>\n"
                             "Для начала нажмите /menu",
                             parse_mode="HTML")
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def get_week_menu(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as user_data:
            # If user_data not filled - fill it
            if not user_data.get('recipes'):
                user_data = await fill_user_data_with_recipes(user_data)
            # If menu does not exist - create it
            if not user_data.get('menu'):
                user_data['menu'] = []

        # If it's callback - send empty answer to finish callback progress bar
        if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
            await message.answer()
            # if it's callback - edit meessage
            await message.message.edit_reply_markup(reply_markup=get_week_menu_kb(menu=user_data.get('menu')))
        else:
            # else - send new message
            await bot.send_photo(chat_id=message.from_user.id, reply_markup=get_week_menu_kb(menu=user_data.get('menu')), photo=open('img/menu.png', 'rb'))
    # If users try to reset already empty menu - cathch exception and do nothing
    except MessageNotModified:
        pass
    # Common exception for all other situations
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def add_day(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as user_data:
            # Create a new day
            user_data['menu'].append({"dishes": []})
            # Fill day with dishes
            for dish_type in dish_types_generator():
                dish = {}
                # Get random recipe from recipe list saved in user_data
                recipe = user_data.get('recipes').get(dish_type)[random.randrange(len(user_data.get('recipes').get(dish_type)))]
                # fill dish with recipe data
                dish['title'] = recipe.title
                dish['recipe_id'] = recipe.id
                dish['type'] = dish_type
                dish['id'] = random.randrange(10000)
                user_data['menu'][-1]['dishes'].append(dish)
            # Edit message with a new day and new dishes
            await call.message.edit_reply_markup(reply_markup=get_week_menu_kb(menu=user_data.get('menu')))
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=call.from_user.id)


async def open_dish(call: types.CallbackQuery, state: FSMContext, dish=None):
    try:
        # anser call to avoid user's progress-bar
        await call.answer()
        async with state.proxy() as user_data:
            # If dish is not passed directly - get it from callback
            if not dish:
                dish = get_dish_by_dish_id(menu=user_data.get('menu'), dish_id=call.data.split('_')[2])
            recipe = get_recipe_by_id(dish.get('recipe_id'))
            ingredients_list = get_ingredients_by_recipe(recipe)
            media = convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
            # Edit message with dish data (photo, title, ingredients)
            await call.message.edit_media(media, reply_markup=get_dish_kb(dish_id=dish.get('id')))
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=call.from_user.id)


async def next_dish(call: types.CallbackQuery, state: FSMContext):
    await change_dish(call=call, state=state, is_increment=True)


async def previous_dish(call: types.CallbackQuery, state: FSMContext):
    await change_dish(call=call, state=state, is_increment=False)


async def change_dish(call: types.CallbackQuery, state: FSMContext, is_increment=True):
    try:
        async with state.proxy() as user_data:
            # Get current dish from callback
            dish = get_dish_by_dish_id(menu=user_data.get('menu'), dish_id=call.data.split('_')[2])
            # Get recipe list from user_data for current dish type
            recipe_list = user_data.get('recipes').get(dish.get('type'))
            # Get current recipe from user_data recipe list
            current_recipe = await get_recipe_from_recipe_list_by_id(recipe_list=recipe_list, recipe_id=dish.get('recipe_id'))
            # Get index of current recipe
            current_recipe_index = recipe_list.index(current_recipe)
            # increment / decrement recipe index
            if is_increment:
                new_recipe_index = await increment_index(recipe_list=recipe_list, current_recipe_index=current_recipe_index)
            else:
                new_recipe_index = await decrement_index(recipe_list=recipe_list, current_recipe_index=current_recipe_index)
            # Get new recipe
            new_recipe = recipe_list[new_recipe_index]
            # Fill dish data from recipe
            dish['title'] = new_recipe.title
            dish['recipe_id'] = new_recipe.id
            await open_dish(call=call, state=state, dish=dish)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=call.from_user.id)


async def increment_index(recipe_list, current_recipe_index):
    new_recipe_index = current_recipe_index + 1
    # Check if recipe index is out of range
    if new_recipe_index >= len(recipe_list):
        new_recipe_index -= len(recipe_list)
    return new_recipe_index


async def decrement_index(recipe_list, current_recipe_index):
    new_recipe_index = current_recipe_index - 1
    # Check if recipe index is out of range
    if new_recipe_index <= 0:
        new_recipe_index += len(recipe_list)
    return new_recipe_index


# Plug for buttons without actions
async def plug(call: types.CallbackQuery):
    # anser call to avoid user's progress-bar
    await call.answer()


# async def cancel_handler(message: types.Message, state: FSMContext):
#     reset_state(state=state)
#     # Cancel state and inform user about it
#     await send_welcome(message)


# Delete all menu data in user_data, then re-open menu
async def reset_menu(call: types.CallbackQuery, state: FSMContext):
    try:
        # anser call to avoid user's progress-bar
        await call.answer()
        async with state.proxy() as user_data:
            user_data['menu'] = []
        await get_week_menu(message=call, state=state)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=call.from_user.id)


async def get_ingredients_list(call: types.CallbackQuery, state: FSMContext):
    try:
        # anser call to avoid user's progress-bar
        await call.answer()
        async with state.proxy() as user_data:
            ingredients_list = await get_dishes_ingredients_list(user_data.get('menu'))
            text = await convert_ingredients_list_to_message_text(ingredients_list)
            await bot.send_message(chat_id=call.from_user.id, text=text, parse_mode='HTML', reply_markup=delete_message_button())
    except MessageTextIsEmpty:
        pass
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=call.from_user.id)


# If user wants to hide ingredients list message - delete it
async def delete_message(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=call.from_user.id)
