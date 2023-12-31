from vcamp.apps.user.models import Recipe, User, FCMDevice


def get_user(filters:dict) -> User:
    try:
        return User.objects.get(**filters)
    except User.DoesNotExist as e:
        raise e
    

def create_user(data:dict) -> User:
    try:
        return User.objects.create(**data)
    except Exception as e:
        raise e


def register_fcm_device(user:User, token:str) -> FCMDevice:
    return FCMDevice.objects.update_or_create(user_id=user.id, defaults={"fcm_token": token})


def get_fcm_token(user:User) -> str | None:
    try:
        return FCMDevice.objects.get(user_id=user.id).fcm_token
    except Exception:
        return None

def create_recipe(data:dict) -> Recipe:
    try:
        return Recipe.objects.create(**data)
    except Exception as e:
        raise e

def bulk_create_recipe(recipe_objs:list) -> Recipe:
    try:
        return Recipe.objects.bulk_create(recipe_objs, ignore_conflicts=True)
    except Exception as e:
        raise e