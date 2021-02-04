import private_storage.urls
from django.contrib import admin
from django.urls import include, path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from apps.django.authentication.sessions import routers as sessions_routers
from apps.django.authentication.user import routers as user_routers
from apps.django.authentication.user.views import (
    LoginView, LogoutView, PasswordChangeView,
)
from apps.django.core.views import contacts
from apps.django.extra.poll import routers as poll_routers
from apps.django.main.course import routers as course_routers
from apps.django.utils.urls import build_patterns


def build_url(prefix: str) -> str:
    return f"api/{prefix}/"


data_patterns = build_patterns("data", [
    sessions_routers.data_router.urls,
    poll_routers.data_router.urls,
    user_routers.data_router.urls,
    course_routers.data_router.urls,
])

relation_patterns = build_patterns("user-relation", [
    course_routers.relation_router.urls,
])

urlpatterns = [
    # Static access
    path("private-media/", include(private_storage.urls)),
    
    # API
    path("api/data/", include("rest_framework.urls")),
    path("api/data/contacts/", contacts),
    # path("api/data/timetable/", timetable),
    # path("api/data/daily-data/", daily_data),
    
    # Autocomplete
    # path("api/autocomplete/homework/type/", HomeworkAutocompleteView.as_view()),
    # path("api/autocomplete/absence/reason/", AbsenceReasonAutocompleteView.as_view()),
    
    # Auth
    path("api/auth/change-password/", PasswordChangeView.as_view()),
    path("api/auth/login/", LoginView.as_view()),
    path("api/auth/logout/", LogoutView.as_view()),
    path("api/auth/reset-password/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    
    path("", include("apps.django.core.urls")),
    path("admin/", admin.site.urls),
    path("", include("user_sessions.urls", "user_sessions")),
    path("api/fcm/devices/", FCMDeviceAuthorizedViewSet.as_view({"post": "create"}), name="create_fcm_device"),
]

urlpatterns += data_patterns
urlpatterns += relation_patterns
