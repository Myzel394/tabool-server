from rest_framework.routers import SimpleRouter

from .views import PollViewSet

__all__ = [
    "student_router", "teacher_router"
]

student_router = SimpleRouter()
student_router.register("poll", PollViewSet, basename="poll")

teacher_router = SimpleRouter()
teacher_router.register("poll", PollViewSet, basename="poll")
