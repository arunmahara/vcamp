import threading
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404

from vcamp.apps.user.models import User

thread_local = threading.local()

class UserLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get("Authorization", "")
        if token.startswith("Bearer "):
            try:
                jwt_token = token.replace("Bearer ", "")
                token = AccessToken(jwt_token)
                user_id = token.payload.get("id")
                user = get_object_or_404(User, id=user_id)
                request.current_user = user
                user_idx = str(user.id)
            except Exception:
                request.current_user = None
                user_idx = None
        else:
            request.current_user = None
            user_idx = None
        thread_local.user_idx = user_idx
        response = self.get_response(request)
        return response