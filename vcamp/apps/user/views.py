from django.http import HttpResponse

from rest_framework import status
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view, permission_classes

from vcamp.apps.user.models import User
from vcamp.apps.user.task.generate_meal import generate_and_save_meal_plan_with_shopping_list, generate_and_save_recipe
from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.helpers.authenticate import authenticate
from vcamp.shared.helpers.generic_reponse import generic_response
from vcamp.apps.user.helpers.generate_token import get_access_token
from vcamp.apps.user.serializers import RecipeSerializer, UserSerializer
from vcamp.apps.user.helpers.sort_meal_plan import sort_according_to_weekday
from vcamp.apps.user.helpers.models_helper import create_user, register_fcm_device


def health(request):
    return HttpResponse("OK")


@api_view(['POST'])
@permission_classes([])
@authenticate()
def signin(request):
    try: 
        user = request.data.get('user')
        
        if not user:              
            decoded_token = request.data.get('decoded_token')
            user_data = {
                'email' : decoded_token['email'],
                'name' : decoded_token.get('name', ''),
                'dp' : decoded_token.get('picture', '')
            }
            
            user = create_user(user_data)

        token = get_access_token(user)
        return generic_response(
            success=True,
            message="Access Token",
            data={"access_token": token},
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        logger.exception(f"Exception on user sign-in: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def register_fcm_token(request):
    try:
        user = request.current_user
        fcm_token = request.data.get('fcm-token')
        
        if fcm_token:
            register_fcm_device(user, fcm_token)

        return generic_response(
            success=True,
            message="FCM Token Registered",
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        logger.exception(f"Exception on register fcm token : {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(["GET"])
def user_profile(request):
    try:
        user = request.current_user
        serializer  = UserSerializer(user)
        return generic_response(
                success=True,
                message="User Profile",
                data=serializer.data,
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.exception(f"Exception on get user profile: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["PATCH"])
def update_profile(request):
    try:
        user = request.current_user

        serializer  = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return generic_response(
                    success=True,
                    message="User Profile Updated",
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
        return generic_response(
                    success=False,
                    message="Invalid Input",
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    except Exception as e:
        logger.exception(f"Exception on update user profile: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def generate_recipe(request):
    try:
        user:User = request.current_user
        ingredients = request.data.get("ingredients")

        if not (ingredients and isinstance(ingredients, list)):
            return generic_response(
                    success=False,
                    message="Invalid Input",
                    data={"ingredients": "Expected a list of items"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        generate_and_save_recipe.delay(user_id=user.id, ingredients=ingredients)
        
        return generic_response(
                success=True,
                message="Recipe Generation Is On Process. You'll Get Notified After Completion.",
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.exception(f"Exception on generate recipe: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_all_recipes(request):
    try:
        user = request.current_user
        recipes = user.user_recipe.all().order_by("-created_at")
        serializer  = RecipeSerializer(recipes, many=True)
        return generic_response(
                success=True,
                message="User Recipes",
                data={"recipes" : serializer.data},
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.exception(f"Exception on get all user recipe : {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(["POST"])
@ratelimit(key='user', rate='1/12h', block=False)
def generate_meal_plan(request):
    try:
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return generic_response(
                success=False,
                message="Limit Exceed! Only 1 meal plan generations are allowed in a day",
                status=status.HTTP_403_FORBIDDEN
            )
        
        user:User = request.current_user

        generate_and_save_meal_plan_with_shopping_list.delay(user.id)

        return generic_response(
                success=True,
                message="Meal Plan Generation Is On Process. You'll Get Notified After Completion.",
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.exception(f"Exception on generate meal plan: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_meal_plan(request):
    try:
        user:User = request.current_user

        if meal_plan := user.week_meal_plan:
            sorted_meal_plan = sort_according_to_weekday(meal_plan)
        else: sorted_meal_plan = None

        return generic_response(
                success=True,
                message="Meal Plan For A Week",
                data={"week_meal_plan" : sorted_meal_plan},
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.exception(f"Exception on get meal plan: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_shopping_list(request):
    try:
        user:User = request.current_user
        return generic_response(
                success=True,
                message="Shopping List For A Week",
                data={"shopping_list_for_week" : user.shopping_list_for_week},
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.exception(f"Exception on get shopping list: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )