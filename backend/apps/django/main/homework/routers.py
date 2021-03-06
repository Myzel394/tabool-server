from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "student_router", "teacher_router", "relation_router"
]

student_router = SimpleRouter()
student_router.register("homework", StudentHomeworkViewSet, basename="homework")
student_router.register("submission", SubmissionViewSet, basename="submission")
student_router.register("material", MaterialViewSet, basename="material")
student_router.register("classbook", ClassbookViewSet, basename="classbook")

teacher_router = SimpleRouter()
teacher_router.register("homework", TeacherHomeworkViewSet, basename="homework")
teacher_router.register("submission", SubmissionViewSet, basename="submission")
teacher_router.register("material", MaterialViewSet, basename="material")
teacher_router.register("classbook", ClassbookViewSet, basename="classbook")

relation_router = SimpleRouter()
relation_router.register("homework", UserHomeworkRelationViewSet, basename="homework-relation")
