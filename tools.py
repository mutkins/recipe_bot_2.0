import itertools
import random
from aiogram.types import InputMediaPhoto
from db.RecipesDB import Recipe, Ingredients
from db.RecipesDB import get_recipe_list_by_dish_type, get_recipe_by_id, get_ingredients_by_recipe


# Generator of dish types. Probably, it should be moved to a config file
def dish_types_generator():
    return ['САЛАТЫ', 'СУПЫ', 'ОСНОВНЫЕ БЛЮДА']


def convert_recipe_and_ingr_obj_to_message(recipe: Recipe, ingredients_list):
    ingredients_srt = ''
    for ingr in ingredients_list:
        ingredients_srt = ingredients_srt + f"<b>{ingr.name}:</b> {ingr.quantity}\n"
    return InputMediaPhoto(media=recipe.recipe_img_url,
                           caption=f'<b><a href="{recipe.recipe_url}">{recipe.title}</a></b>, {recipe.time_text}\n\n'
                                   f'{ingredients_srt}', parse_mode='HTML')


def get_dish_by_dish_id(menu, dish_id):
    for day in menu:
        for dish in day.get('dishes'):
            if str(dish.get('id')) == dish_id:
                return dish


async def fill_user_data_with_recipes(user_data):
    user_data['recipes'] = {}
    for dish_type in dish_types_generator():
        user_data['recipes'][dish_type] = get_recipe_list_by_dish_type(dish_type)
    for dish_type in user_data.get('recipes'):
        random.shuffle(user_data.get('recipes').get(dish_type))
        for rec in user_data.get('recipes').get(dish_type):
            print(rec.title)
    return user_data


async def get_recipe_from_recipe_list_by_id(recipe_list, recipe_id):
    for recipe in recipe_list:
        if recipe.id == recipe_id:
            return recipe


async def get_dishes_ingredients_list(menu):
    dishes_ingredients_list = []
    for day in menu:
        for dish in day.get('dishes'):
            recipe = get_recipe_by_id(dish.get('recipe_id'))
            ingredients = get_ingredients_by_recipe(recipe)
            dishes_ingredients_list = merging_lists(dishes_ingredients_list, ingredients)
    return dishes_ingredients_list


# The goal if this function - to sum two lists of ingredients. If  lists have the same ingredients - they will be merged
def merging_lists(list1, list2):
    # if one of lists is empty - return other
    if not list1:
        return list2
    if not list2:
        return list1
    final_list = []
    for item_from_l1, item_from_l2 in itertools.zip_longest(list1, list2):
        # If one of lists is empty - return other (because there is nothin to merge
        if item_from_l1 is None:
            final_list.append(item_from_l2)
            continue
        if item_from_l2 is None:
            final_list.append(item_from_l1)
            continue
        if item_from_l1.get('name') == item_from_l2.get('name'):
            quantity = f"{item_from_l1.get('quantity')} + {item_from_l2.get('quantity')}"
            final_list.append({'name': item_from_l1.get('name'), 'quantity': quantity})
        else:
            final_list.append(item_from_l1)
            final_list.append(item_from_l2)
    return final_list


async def convert_ingredients_list_to_message_text(ingredients_list):
    message_text = ""
    for ingr in ingredients_list:
        message_text += f"<b>{ingr.get('name')}:</b> {ingr.get('quantity')}\n"
    return message_text