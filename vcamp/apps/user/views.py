from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from vcamp.apps.user.helpers.generate_recipe import generate_recipe_form_prompt
from vcamp.apps.user.models import Recipe, User
from vcamp.apps.user.services.edenai import EdenAIService

from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.serializers import RecipeSerializer, UserSerializer
from vcamp.apps.user.helpers.authenticate import authenticate
from vcamp.shared.helpers.generic_reponse import generic_response
from vcamp.apps.user.helpers.generate_token import get_access_token
from vcamp.apps.user.helpers.models_helper import create_user, register_fcm_device, bulk_create_recipe


def vcamp(request):
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
            additional_data={"access_token": token},
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
        logger.exception(f"Exception on set fcm token : {e}")
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
        logger.exception(f"Exception on user profile: {e}")
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
        logger.exception(f"Exception on user profile update: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def generate_recipe(request):
    try:
        user: User = request.current_user
        ingredients = request.data.get("ingredients")

        if not (ingredients and isinstance(ingredients, list)):
            return generic_response(
                    success=False,
                    message="Invalid Input",
                    data={"ingredients": "Expected a list of items"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        preferences = user.preferences
        allergies = user.allergies
        dietary_restrictions = user.dietary_restrictions

        recipes = generate_recipe_form_prompt(preferences, allergies, dietary_restrictions, ingredients)

        recipe_objs = []
        for recipe in recipes["recipes"]:
            name = recipe["name"]
            ingredients = recipe["ingredients"]
            measurements = recipe["measurements"]
            process = recipe["process"]
            recipe_image = EdenAIService().generate_image(name)
            recipe_objs.append(Recipe(user_id=user.id, name=name, ingredients=ingredients, measurements=measurements, process=process, image=recipe_image))

        querysets = bulk_create_recipe(recipe_objs)
        serializer  = RecipeSerializer(querysets, many=True)
        return generic_response(
                success=True,
                message="List of Recipes",
                data={"recipes" : serializer.data},
                status=status.HTTP_200_OK
            )
    
    except Exception as e:
        logger.exception(f"Exception on generate recipe: {e}")
        return generic_response(
            success=False,
            message="Something Went Wrong!",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

