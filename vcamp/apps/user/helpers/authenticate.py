from rest_framework import status
import firebase_admin
from firebase_admin import credentials,auth

from vcamp.shared.helpers.logging_helper import logger
from vcamp.apps.user.helpers.models_helper import get_user
from vcamp.shared.helpers.generic_reponse import generic_response

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_app = firebase_admin.initialize_app(cred)


def authenticate():
    def decorator(func):
        def wrapper(*args, **kwargs):
            token = args[-1].data.get('token', None)
            
            if not token:
                return generic_response(success=False, message="No Auth Token", status=status.HTTP_400_BAD_REQUEST)
            
            try:
                decoded_token = auth.verify_id_token(token)
                args[-1].data['decoded_token'] = decoded_token
            
            except auth.ExpiredIdTokenError:
                logger.info('Login Token Expired')
                return generic_response(success=False, message="Auth Token Expired", status=status.HTTP_400_BAD_REQUEST)
                
            except Exception as err:
                logger.error(f"Exception in Firebase Authentication: {err}")
                return generic_response(success=False, message="Invalid Auth Token", status=status.HTTP_400_BAD_REQUEST)

            try:
                user = get_user({"email":decoded_token['email']})
                args[-1].data['user'] = user

            except:
                args[-1].data['user'] = None
            
            return func(*args,  **kwargs)
        return wrapper
    return decorator