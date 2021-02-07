from rest_framework.throttling import UserRateThrottle

__all__ = [
    "BurstDayViewThrottle", "SustainedDayViewThrottle"
]


class BurstDayViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "burst_day": "30/min"
    }
    scope = "burst_day"


class SustainedDayViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "sustained_day": "500/day"
    }
    scope = "sustained_day"
