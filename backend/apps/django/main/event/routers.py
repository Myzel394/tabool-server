from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "student_router", "teacher_router"
]

student_router = SimpleRouter()
student_router.register("event", EventViewSet, basename="event")
student_router.register("exam", ExamViewSet, basename="exam")
student_router.register("modification", ModificationViewSet, basename="modification")

teacher_router = SimpleRouter()
teacher_router.register("event", EventViewSet, basename="event")
teacher_router.register("exam", ExamViewSet, basename="exam")
teacher_router.register("modification", ModificationViewSet, basename="modification")
