from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "data_router"
]

data_router = SimpleRouter()
data_router.register("session", SessionViewSet, basename="session")
