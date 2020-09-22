from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.event.sub.subviews import ClassTestViewSet, EventUserOptionViewSet, EventViewSet
from apps.homework.views import TeacherHomeworkViewSet, UserHomeworkViewSet
from apps.timetable.views import TimetableViewSet

router = DefaultRouter()
router.register("timetable", TimetableViewSet, basename="TimeTable")
router.register("teacher-homework", TeacherHomeworkViewSet, basename="TeacherHomework")
router.register("user-homework", UserHomeworkViewSet, basename="UserHomework")
router.register("class-test", ClassTestViewSet, basename="ClassTest")
router.register("event", EventViewSet, basename="Event")
router.register("event-user-option", EventUserOptionViewSet, basename="EventUserOption")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/", include(router.urls))
]
