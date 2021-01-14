import private_storage.urls
from django.contrib import admin
from django.urls import include, path

from apps.django.core.views import contacts
from apps.django.main.authentication.sub.subviews.apis.register import FullRegisterView, RegisterView
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
    path(f"api/data/", include("rest_framework.urls")),
    path(f"api/data/contacts/", contacts),
    path(f"api/data/timetable/", timetable),
    path(f"api/data/daily-data/", daily_data),
    
    # Autocomplete
    path(f"api/autocomplete/homework/type/", HomeworkAutocompleteView.as_view()),
    
    path(f"api/auth/change-password/", PasswordChangeView.as_view()),
    path(f"api/auth/registration/", RegisterView.as_view()),
    path(f"api/auth/full-registration/", FullRegisterView.as_view()),
    path(f"api/auth/login/", LoginView.as_view()),
    path(f"api/auth/logout/", LogoutView.as_view()),
    path(f"api/auth/confirmation/", EmailConfirmation.as_view()),
    
    path("", include("apps.django.core.urls")),
    path("admin/", admin.site.urls),
    path("", include("user_sessions.urls", "user_sessions"))
]

urlpatterns += data_patterns
urlpatterns += relation_patterns
