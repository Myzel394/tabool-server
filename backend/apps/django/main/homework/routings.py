from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import *

__all__ = [
    "data_router", "homework_router", "homework_history_router", "relation_router"
]

data_router = SimpleRouter()
data_router.register("material", MaterialViewSet, basename="material")
data_router.register("submission", SubmissionViewSet, basename="submission")

homework_router = SimpleRouter()
homework_router.register("homework", HomeworkViewSet, basename="homework")

homework_history_router = NestedSimpleRouter(homework_router, "homework", lookup="homework")
homework_history_router.register("history", HomeworkHistoryViewSet, basename="history")

relation_router = SimpleRouter()
relation_router.register("homework", UserHomeworkRelationViewSet, basename="homework-relation")
