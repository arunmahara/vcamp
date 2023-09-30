from rest_framework_simplejwt.tokens import RefreshToken

from vcamp.apps.user.models import User


def get_access_token(user:User) -> str:
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)