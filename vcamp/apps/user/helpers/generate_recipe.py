import json

from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.services.edenai import EdenAIService
from vcamp.apps.user.utils.response_format import recipe_response_format


def generate_recipe_form_prompt(preferences:list, allergies:list, dietary_restrictions:list, ingredients:list) -> dict:
    prompt= (
        "Considering an individual with the following "
        f"preferences: {preferences}, allergies: {allergies}, and dietary restrictions: {dietary_restrictions} " 
        f"provide one recipes that incorporate the ingredients {ingredients}."
        "Each recipe should include the dish name, ingredients, measurements, and a step-by-step process for preparation. \n"
        "Respose should strictly be in json format like give below and don't change the key of json. \n" +
        str(recipe_response_format)

    )

    recipes = EdenAIService().generate_reply(prompt)
    try:
        recipes_dict = json.loads(recipes[recipes.index('{'):])
        return recipes_dict
    except Exception as e :
        logger.info(f"Could Not Parse Recipe: {e}")
        return generate_recipe_form_prompt(preferences, allergies, dietary_restrictions, ingredients)