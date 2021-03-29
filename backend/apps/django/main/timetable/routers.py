from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "student_router", "teacher_router"
]

student_router = SimpleRouter()
student_router.register("timetable", StudentTimetableViewSet, basename="timetable")

teacher_router = SimpleRouter()
teacher_router.register("timetable", TeacherTimetableViewSet, basename="timetable")
