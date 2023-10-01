from uuid import UUID

from celery import shared_task

from vcamp.apps.user.models import Recipe, User
from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.services.edenai import EdenAIService
from vcamp.apps.user.task.push_notification import sendPushNotification
from vcamp.apps.user.helpers.models_helper import bulk_create_recipe, create_recipe, get_fcm_token, get_user
from vcamp.apps.user.helpers.generate_dish import generate_meal_plan_form_prompt, generate_recipe_form_prompt, generate_shopping_list_form_prompt



def get_preferences(user:User):
    preferences = user.preferences
    allergies = user.allergies
    dietary_restrictions = user.dietary_restrictions
    return preferences, allergies, dietary_restrictions


def notify_user(user: User, title: str, message: str, image: str = "") -> None:
    if fcm_token := get_fcm_token(user):
        sendPushNotification(title, message, [fcm_token], image)


@shared_task(name="generate_and_save_recipe")
def generate_and_save_recipe(user_id:UUID, ingredients:list) -> None:
    try:
        user = get_user({"id":user_id})
        
        preferences, allergies, dietary_restrictions = get_preferences(user)
        if not (preferences, allergies, dietary_restrictions):
            notify_user(user, "Recipe Generation Failed!", "Please provide preferences, allergies and dietary_restrictions.")
            return 
        
        recipes = generate_recipe_form_prompt(preferences, allergies, dietary_restrictions, ingredients)

        # recipe_objs = []
        for recipe in recipes["recipes"]:
            name = recipe["name"]
            nutrition = recipe["nutrition"]
            ingredients = recipe["ingredients"]
            measurements = recipe["measurements"]
            process = recipe["process"]
            recipe_image = EdenAIService().generate_image(name)
            # recipe_objs.append(Recipe(user_id=user.id, name=name, nutrition=nutrition, ingredients=ingredients, measurements=measurements, process=process, image=recipe_image))
            recipe = create_recipe({"user_id":user.id, "name":name, "nutrition":nutrition, "ingredients":ingredients, "measurements":measurements, "process":process, "image":recipe_image})
            recipe_image = recipe.image
            notify_user(user, "Recipe Is Ready", name, recipe_image)

        # bulk_create_recipe(recipe_objs)
        return

    except Exception as e :
        logger.info(f"Exception while generating recipe: {e}")
        return generate_and_save_recipe(user_id, ingredients)


@shared_task(name="generate_and_save_meal_plan_with_shopping_list")
def generate_and_save_meal_plan_with_shopping_list(user_id:UUID) -> None:
    try:
        user = get_user({"id":user_id})
        preferences, allergies, dietary_restrictions = get_preferences(user)
        if not (preferences, allergies, dietary_restrictions):
            notify_user(user, "Meal Plan Generation Failed!", "Please provide preferences, allergies and dietary_restrictions.")
            return 

        meal_plan = generate_meal_plan_form_prompt(preferences, allergies, dietary_restrictions)

        user.week_meal_plan = meal_plan
        user.save()
        notify_user(user, "Meal Plan Is Ready", "Go to app to view meal plan.")
        generate_and_save_shopping_list.delay(user.id)

    except Exception as e :
        logger.info(f"Exception while generating meal plan: {e}")
        return generate_and_save_meal_plan_with_shopping_list(user_id)


@shared_task(name="generate_and_save_shopping_list")
def generate_and_save_shopping_list(user_id:UUID) -> None:
    try:
        user = get_user({"id":user_id})
        ingredients = user.week_meal_plan.get("ingredients")
        if ingredients:
            shopping_list = generate_shopping_list_form_prompt(ingredients)
            user.shopping_list_for_week  = shopping_list
            notify_user(user, "Shopping List Is Ready", "Go to app to view shopping list.")
        return

    except Exception as e :
        logger.info(f"Exception while generating shopping list: {e}")
        return generate_shopping_list_form_prompt(ingredients)