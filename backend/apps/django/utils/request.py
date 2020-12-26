from django_hint import RequestType

from apps.django.utils import constants as utils_constants

__all__ = [
    "request_prefers_id", "get_client_ip"
]


def request_prefers_id(request: RequestType, key: str, object_id: str) -> bool:
    if preferred_ids := request.META.get(utils_constants.PREFERRED_IDS_HEADER_NAME):
        if value := preferred_ids.get(key):
            return object_id in value
    
    return False


def get_client_ip(request: RequestType) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
