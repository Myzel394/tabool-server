from rest_framework.routers import SimpleRouter

from .views import *

__all__ = [
    "data_router", "relation_router"
]

data_router = SimpleRouter()
data_router.register("room", RoomViewSet, basename="room")
data_router.register("subject", SubjectViewSet, basename="subject")
data_router.register("teacher", TeacherViewSet, basename="teacher")

relation_router = SimpleRouter()
relation_router.register("subject", UserSubjectRelationViewSet, "subject-relation")
