from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import *

__all__ = [
    "classtest_router", "classtest_history_router", "data_router", "relation_router"
]

classtest_router = SimpleRouter()
classtest_router.register("classtest", ClasstestViewSet, basename="classtest")

classtest_history_router = NestedSimpleRouter(classtest_router, "classtest", lookup="classtest")
classtest_history_router.register("history", ClasstestHistoryViewSet, basename="classtest-history")

data_router = SimpleRouter()
data_router.register("modification", ModificationViewSet, basename="modification")
data_router.register("event", EventViewSet, basename="event")

relation_router = SimpleRouter()
relation_router.register("event", EventUserRelationViewSet, basename="event-relation")
