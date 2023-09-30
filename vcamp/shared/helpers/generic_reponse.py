from rest_framework.response import Response


def generic_response(success:bool|None=None, message:str|None=None, data:dict|None=None, status:int|None=None, additional_data:dict|None=None) -> Response:
    """
    Generic API response structure.
    Returns response with same format for all apis.
    """
    if not additional_data:
        additional_data = {}

    response_body = {
        "success": success,
        "message": message,
        **additional_data,
        "data": data or {},
      }
    
    return Response(response_body, status)