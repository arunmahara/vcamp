from django.utils import timezone
from vcamp.shared.helpers.logging_helper import logger


def sort_according_to_weekday(meal_plan:dict) -> dict:
    try: 
        local_time = timezone.now().astimezone(timezone.get_current_timezone())
        current_day_index = local_time.weekday()

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        sorted_weekdays = weekdays[current_day_index:] + weekdays[:current_day_index]

        sorted_meal_plan = {
            "ingredients": meal_plan["ingredients"]
        }

        for day in sorted_weekdays:
            sorted_meal_plan[day] = meal_plan[day]
        
        return sorted_meal_plan

    except Exception as e:
        logger.exception(f"Exception while sorting meal plan: {e}")
        raise e