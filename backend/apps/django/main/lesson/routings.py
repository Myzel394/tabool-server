from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "data_router", "relation_router"
]

data_router = SimpleRouter()
data_router.register("course", CourseViewSet, basename="course")
data_router.register("lesson", LessonViewSet, basename="lesson")

relation_router = SimpleRouter()
relation_router.register("lesson", UserLessonRelationViewSet, basename="lesson-relation")
