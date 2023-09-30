from django.urls import path
from . import views


urlpatterns = [
    path('auth/', views.signin, name='signin'),
    path('set-fcm-token/', views.register_fcm_token, name='register_fcm_token'),
    path('user-profile/', views.user_profile, name='user_profile'),
]