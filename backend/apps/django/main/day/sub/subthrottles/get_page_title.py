from rest_framework.throttling import UserRateThrottle

__all__ = [
    "BurstGetPageTitleViewThrottle", "SustainedGetPageTitleViewThrottle"
]


class BurstGetPageTitleViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "burst_get_head": "120/min"
    }
    scope = "burst_get_head"


class SustainedGetPageTitleViewThrottle(UserRateThrottle):
    THROTTLE_RATES = {
        "sustained_get_head": "500/day"
    }
    scope = "sustained_get_head"
