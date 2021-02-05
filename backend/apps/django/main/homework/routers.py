from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "student_router", "teacher_router"
]

data_router = SimpleRouter()
data_router.register("classbook", ClassbookViewSet, basename="classbook")

student_router = SimpleRouter()
student_router.register("homework", StudentHomeworkViewSet, basename="homework")
student_router.register("submission", SubmissionViewSet, basename="submission")

teacher_router = SimpleRouter()
teacher_router.register("homework", TeacherHomeworkViewSet, basename="homework")
teacher_router.register("material", MaterialViewSet, basename="material")
