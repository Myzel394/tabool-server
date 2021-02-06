from rest_framework.throttling import UserRateThrottle

__all__ = [
    "LessonViewThrottle"
]


class LessonViewThrottle(UserRateThrottle):
    THROTTLE_RATES = "30/min"
