import json

from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.services.edenai import EdenAIService
from vcamp.apps.user.utils.response_format import recipe_response_format, meal_plan_response_format, shopping_list_response_format


def generate_recipe_form_prompt(preferences:list, allergies:list, dietary_restrictions:list, ingredients:list) -> dict:
    prompt= (
        "Considering an individual with the following "
        f"preferences: {preferences}, allergies: {allergies}, and dietary restrictions: {dietary_restrictions} " 
        f"provide one recipe that incorporate the ingredients {ingredients}."
        "Each recipe should include the dish name, nutrition information, ingredients, measurements, and a step-by-step process for preparation. \n"
        "Response should strictly be in json format like give below and don't change the key of json. \n" +
        str(recipe_response_format)

    )

    recipes = EdenAIService().generate_reply(prompt)
    try:
        return json.loads(recipes[recipes.index('{'):])
    except Exception as e :
        logger.info(f"Could Not Parse Recipe: {e}")
        return generate_recipe_form_prompt(preferences, allergies, dietary_restrictions, ingredients)
    

def generate_meal_plan_form_prompt(preferences:list, allergies:list, dietary_restrictions:list) -> dict:
    prompt= (
        "Considering an individual with the following " 
        f"preferences: {preferences}, allergies: {allergies}, and dietary restrictions: {dietary_restrictions} "
        "plan meals for a week and generate a consolidated list of ingredients needed for the week. "
        "Please ensure to include the dish names, nutrition information and any specific ingredients or quantities required for each meal. \n"
        "Response should strictly be in json format like give below and don't change the key of json. \n" +
        str(meal_plan_response_format)

    )

    meal_plan = EdenAIService().generate_reply(prompt)
    try:
        return json.loads(meal_plan[meal_plan.index('{'):])
    except Exception as e :
        logger.info(f"Could Not Parse Recipe: {e}")
        return generate_meal_plan_form_prompt(preferences, allergies, dietary_restrictions)


def generate_shopping_list_form_prompt(ingredients:list) -> dict:
    prompt= (
        f"Using the given list of ingredients {ingredients}, create a comprehensive shopping list for one week, "
        "including precise measurements, and make sure to identify any missing ingredients. \n"
        "Response should strictly be in json format like give below and don't change the key of json. \n" +
        str(shopping_list_response_format)

    )

    shopping_list = EdenAIService().generate_reply(prompt)
    try:
        return json.loads(shopping_list[shopping_list.index('{'):])
    except Exception as e :
        logger.info(f"Could Not Parse Recipe: {e}")
        return generate_shopping_list_form_prompt(ingredients)