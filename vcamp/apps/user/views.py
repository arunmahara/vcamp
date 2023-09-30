from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.helpers.authenticate import authenticate
from vcamp.shared.helpers.generic_reponse import generic_response
from vcamp.apps.user.helpers.generate_token import get_access_token
from vcamp.apps.user.helpers.models_helper import create_user


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