from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.homework.views import TeacherHomeworkViewSet, UserHomeworkViewSet
from apps.timetable.views import TimeTableViewSet

router = DefaultRouter()
router.register("timetable", TimeTableViewSet, basename="TimeTable")
router.register("teacher-homework", TeacherHomeworkViewSet, basename="TeacherHomework")
router.register("user-homework", UserHomeworkViewSet, basename="UserHomework")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/", include(router.urls))
]
