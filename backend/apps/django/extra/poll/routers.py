from rest_framework.routers import SimpleRouter

from .views import PollViewSet

__all__ = [
    "data_router"
]

data_router = SimpleRouter()
data_router.register("poll", PollViewSet, basename="material")
