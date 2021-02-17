from rest_framework.throttling import UserRateThrottle

__all__ = [
    "BurstDailyDataViewThrottle", "SustainedDailyDataViewThrottle"
]


class BurstDailyDataViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "burst_daily_data": "30/min"
    }
    scope = "burst_daily_data"


class SustainedDailyDataViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "sustained_daily_data": "400/day"
    }
    scope = "sustained_daily_data"
