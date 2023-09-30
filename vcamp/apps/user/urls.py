from django.urls import path
from . import views


urlpatterns = [
    path('auth/', views.signin, name='signin'),
    path('set-fcm-token/', views.register_fcm_token, name='register_fcm_token'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/update-profile/', views.update_profile, name='update_profile'),
    path('meal/generate-recipe/', views.generate_recipe, name='generate_recipe'),
    path('user/recipes/', views.get_all_recipes, name='user_recipes'),
    path('meal/generate-meal-plan/', views.generate_meal_plan, name='generate_meal_plan'),
    path('user/meal-plan/', views.get_meal_plan, name='user_meal_plan'),
    path('user/shopping-list/', views.get_shopping_list, name='user_shopping_list'),
]