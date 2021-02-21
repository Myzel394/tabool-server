from rest_framework.throttling import UserRateThrottle

__all__ = [
    "BurstGetHeadViewThrottle", "SustainedGetHeadViewThrottle"
]


class BurstGetHeadViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "burst_get_head": "120/min"
    }
    scope = "burst_get_head"


class SustainedGetHeadViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "sustained_get_head": "500/day"
    }
    scope = "sustained_get_head"
