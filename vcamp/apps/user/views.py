from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.serializers import UserSerializer
from vcamp.apps.user.helpers.authenticate import authenticate
from vcamp.shared.helpers.generic_reponse import generic_response
from vcamp.apps.user.helpers.generate_token import get_access_token
from vcamp.apps.user.helpers.models_helper import create_user, register_fcm_device


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