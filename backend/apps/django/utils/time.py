from datetime import datetime, timedelta

from django.conf import settings

__all__ = [
    "get_now"
]


def get_now() -> datetime:
    now = datetime.now() - timedelta(seconds=settings.NOW_THRESHOLD)
    
    return now
