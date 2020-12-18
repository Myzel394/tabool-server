from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import *

__all__ = [
    "exam_router", "exam_history_router", "data_router", "relation_router"
]

exam_router = SimpleRouter()
exam_router.register("exam", ExamViewSet, basename="exam")

exam_history_router = NestedSimpleRouter(exam_router, "exam", lookup="exam")
exam_history_router.register("history", ExamHistoryViewSet, basename="exam-history")

data_router = SimpleRouter()
data_router.register("modification", ModificationViewSet, basename="modification")
data_router.register("event", EventViewSet, basename="event")

relation_router = SimpleRouter()
relation_router.register("event", EventUserRelationViewSet, basename="event-relation")
