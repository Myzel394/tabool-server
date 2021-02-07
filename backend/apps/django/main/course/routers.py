from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "student_router", "teacher_router", "relation_router"
]

student_router = SimpleRouter()
student_router.register("room", RoomViewSet, basename="room")
student_router.register("subject", SubjectViewSet, basename="subject")
student_router.register("course", CourseViewSet, basename="course")

teacher_router = SimpleRouter()
teacher_router.register("room", RoomViewSet, basename="room")
teacher_router.register("subject", SubjectViewSet, basename="subject")
teacher_router.register("course", CourseViewSet, basename="course")

relation_router = SimpleRouter()
relation_router.register("subject", UserSubjectRelationViewSet, "subject-relation")
