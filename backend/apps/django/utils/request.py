from django_hint import RequestType

from apps.django.utils import constants as utils_constants

__all__ = [
    "request_prefers_id"
]


def request_prefers_id(request: RequestType, key: str, object_id: str) -> bool:
    if preferred_ids := request.META.get(utils_constants.PREFERRED_IDS_HEADER_NAME):
        if value := preferred_ids.get(key):
            return object_id in value
    
    return False
