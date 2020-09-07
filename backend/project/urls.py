from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from apps.timetable.views import LessonViewSet

router = routers.DefaultRouter()
router.register("timetable", LessonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/", include(router.urls))
]
