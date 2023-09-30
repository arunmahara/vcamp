from uuid import UUID

from celery import shared_task

from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.helpers.models_helper import get_user
from vcamp.apps.user.helpers.generate_dish import generate_shopping_list_form_prompt


@shared_task(name="generate_and_save_shopping_list")
def generate_and_save_shopping_list(user_id:UUID) -> None:
    try:
        user = get_user({"id":user_id})
        ingredients = user.week_meal_plan.get("ingredients")
        if ingredients:
            shopping_list = generate_shopping_list_form_prompt(ingredients)
            user.shopping_list_for_week  = shopping_list
            user.save()
        return

    except Exception as e :
        logger.info(f"Exception while generating shopping list: {e}")
        return generate_shopping_list_form_prompt(ingredients)