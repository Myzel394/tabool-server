from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "student_router", "teacher_router"
]
student_router = SimpleRouter()
student_router.register("user", UserViewSet, basename="user")
student_router.register("preference", PreferenceViewSet, basename="preference")
student_router.register("teacher", TeacherViewSet, basename="teacher")

teacher_router = SimpleRouter()
teacher_router.register("user", UserViewSet, basename="user")
teacher_router.register("preference", PreferenceViewSet, basename="preference")
