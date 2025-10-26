from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def _to_details(data):
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        return {'non_field_errors': data}
    return {'detail': data}

def custom_exception_handler(exc, context):
    resp = exception_handler(exc, context)

    if resp is None:
        return Response(
            {
                'error': {
                    'type': exc.__class__.__name__,
                    'details': {'detail': 'Internal server error'}
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    payload = {
        'error': {
            'type': exc.__class__.__name__,
            'details': _to_details(resp.data),
        }
    }
    return Response(payload, status=resp.status_code, headers=resp.headers)
