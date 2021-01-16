import private_storage.urls
from django.contrib import admin
from django.urls import include, path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from apps.django.core.views import contacts
from apps.django.main.authentication.sub.subviews.apis.register import FullRegisterView, RegisterView
from apps.django.main.authentication.sub.subviews.apis.scooso_credentials import ScoosoCredentialsView
from apps.django.main.authentication.views import (
    EmailConfirmation, LoginView, LogoutView, PasswordChangeView,
)
from apps.django.main.event import routers as event_routers
from apps.django.main.homework import routers as homework_routers
from apps.django.main.homework.views import HomeworkAutocompleteView
from apps.django.main.lesson import routers as lesson_routers
from apps.django.main.lesson.views import daily_data, timetable
from apps.django.main.school_data import routers as school_routers
from apps.django.main.sessions import routers as sessions_routers
from apps.django.utils.urls import build_patterns


def build_url(prefix: str) -> str:
    return f"api/{prefix}/"


data_patterns = build_patterns("data", [
    event_routers.data_router.urls,
    event_routers.exam_router.urls,
    event_routers.exam_history_router.urls,
    homework_routers.data_router.urls,
    homework_routers.homework_router.urls,
    homework_routers.homework_history_router.urls,
    lesson_routers.data_router.urls,
    school_routers.data_router.urls,
    sessions_routers.data_router.urls
])

relation_patterns = build_patterns("user-relation", [
    event_routers.relation_router.urls,
    homework_routers.relation_router.urls,
    lesson_routers.relation_router.urls,
    school_routers.relation_router.urls
])

urlpatterns = [
    # Static access
    path("private-media/", include(private_storage.urls)),
    
    # API
    path("api/data/", include("rest_framework.urls")),
    path("api/data/contacts/", contacts),
    path("api/data/timetable/", timetable),
    path("api/data/daily-data/", daily_data),
    
    # Autocomplete
    path("api/autocomplete/homework/type/", HomeworkAutocompleteView.as_view()),
    
    path("api/auth/change-password/", PasswordChangeView.as_view()),
    path("api/auth/scooso-credentials/", ScoosoCredentialsView.as_view()),
    path("api/auth/registration/", RegisterView.as_view()),
    path("api/auth/full-registration/", FullRegisterView.as_view()),
    path("api/auth/login/", LoginView.as_view()),
    path("api/auth/logout/", LogoutView.as_view()),
    path("api/auth/confirmation/", EmailConfirmation.as_view()),
    path("api/auth/reset-password/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    
    path("", include("apps.django.core.urls")),
    path("admin/", admin.site.urls),
    path("", include("user_sessions.urls", "user_sessions")),
    path("api/fcm/devices/", FCMDeviceAuthorizedViewSet.as_view({"post": "create"}), name="create_fcm_device"),
]

urlpatterns += data_patterns
urlpatterns += relation_patterns
