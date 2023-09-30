from vcamp.apps.user.models import User


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