from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.timetable.views import TimeTableViewSet

router = DefaultRouter()
router.register("timetable", TimeTableViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/", include(router.urls))
]
