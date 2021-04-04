import re

import requests
from django.views.decorators.cache import cache_page
from django_hint import RequestType
from requests.adapters import HTTPAdapter
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from urllib3.util.retry import Retry

from apps.django.utils.permissions import AuthenticationAndActivePermission
from ....serializers import GetPageTitleSerializer
from ....throttles import BurstGetPageTitleViewThrottle, SustainedGetPageTitleViewThrottle

__all__ = [
    "get_page_title_view"
]

ONE_MONTH_IN_SECONDS = 60 * 60 * 24 * 30

headers = {
    "User-Agent": "TitleGrabber@tabool"
}

retries = Retry(
    total=5,
    backoff_factor=0.4,
)
retries.BACKOFF_MAX = 1
session = requests.Session()
session.headers.update(headers)
session.mount("https://", HTTPAdapter(max_retries=retries))
regex = re.compile('<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)


@cache_page(ONE_MONTH_IN_SECONDS)
@api_view(["GET"])
@permission_classes([AuthenticationAndActivePermission])
@throttle_classes([BurstGetPageTitleViewThrottle, SustainedGetPageTitleViewThrottle])
def get_page_title_view(request: RequestType):
    serializer = GetPageTitleSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data
    url = validated_data["url"]

    response = session.get(url)

    if not (200 <= response.status_code < 300):
        return Response({
            "detail": f"Server responded with status code '{response.status_code}'.",
            "status_code": response.status_code,
            "code": "blocked" if response.status_code == 429 else "failed"
        }, status=status.HTTP_502_BAD_GATEWAY)

    try:
        html = response.text
        title = regex.search(html).group(1)
    except Exception:
        return Response({
            "detail": "Title couldn't be found.",
            "code": "title_not_found"
        }, status=status.HTTP_502_BAD_GATEWAY)
    
    return Response({
        "title": title
    })
