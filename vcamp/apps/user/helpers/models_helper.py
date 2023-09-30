from vcamp.apps.user.models import User, FCMDevice


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