from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "data_router"
]

data_router = SimpleRouter()
data_router.register("course", CourseViewSet, basename="course")
data_router.register("lesson", LessonViewSet, basename="lesson")
data_router.register("lesson-absence", LessonAbsenceView, basename="lesson_absence")
