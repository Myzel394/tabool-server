from rest_framework.throttling import UserRateThrottle

__all__ = [
    "BurstWeekViewThrottle", "SustainedWeekViewThrottle"
]


class BurstWeekViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "burst_day": "40/min"
    }
    scope = "burst_day"


class SustainedWeekViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "sustained_day": "500/day"
    }
    scope = "sustained_day"
