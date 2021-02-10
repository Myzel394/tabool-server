from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "auth_router"
]

auth_router = SimpleRouter()
auth_router.register("session", SessionViewSet, basename="session")
