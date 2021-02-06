from rest_framework.throttling import UserRateThrottle

__all__ = [
    "BurstDayViewThrottle", "SustainedDayViewThrottle"
]


class BurstDayViewThrottle(UserRateThrottle):
    THROTTLE_RATES = "10/min"


class SustainedDayViewThrottle(UserRateThrottle):
    THROTTLE_RATES = "200/day"
