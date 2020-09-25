from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.authentication.views import LoginView, LogoutView, PasswordChangeView, RegisterView
from apps.event.views import ClassTestViewSet, EventViewSet
from apps.homework.views import UserHomeworkViewSet
from apps.timetable.views import TimetableViewSet

router = DefaultRouter()
router.register("timetable", TimetableViewSet, basename="TimeTable")
router.register("user-homework", UserHomeworkViewSet, basename="UserHomework")
router.register("class-test", ClassTestViewSet, basename="ClassTest")
router.register("event", EventViewSet, basename="Event")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("api/change-password/", PasswordChangeView.as_view()),
    path("api/registration/", RegisterView.as_view()),
    path("api/registration/", LoginView.as_view()),
    path("api/registration/logout/", LogoutView.as_view()),
]
