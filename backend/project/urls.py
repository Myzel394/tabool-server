import private_storage.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.django.main.authentication.views import (
    email_confirmation, LoginView, LogoutView, PasswordChangeView, RegisterView, StudentView,
)
from apps.django.main.event import routings as event_routers
from apps.django.main.homework import routings as homework_routers
from apps.django.main.homework.views import (
    MaterialDownloadView,
)
from apps.django.main.lesson import routings as lesson_routers
from apps.django.main.school_data import routings as school_routers
from apps.django.utils.urls import build_patterns
from constants.api import API_VERSION


def build_url(prefix: str) -> str:
    return f"api/{API_VERSION}/{prefix}/"


data_patterns = build_patterns("data", [
    event_routers.data_router.urls,
    event_routers.classtest_router.urls,
    event_routers.classtest_history_router.urls,
    homework_routers.data_router.urls,
    homework_routers.homework_router.urls,
    homework_routers.homework_history_router.urls,
    lesson_routers.data_router.urls,
    school_routers.data_router.urls
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
    path("materials-media/", MaterialDownloadView.as_view()),
    
    # API
    path(f"api/{API_VERSION}/data/", include("rest_framework.urls")),
    
    path(f"api/{API_VERSION}/auth/change-password/", PasswordChangeView.as_view()),
    path(f"api/{API_VERSION}/auth/registration/", RegisterView.as_view()),
    path(f"api/{API_VERSION}/auth/student/", StudentView.as_view()),
    path(f"api/{API_VERSION}/auth/login/", LoginView.as_view()),
    path(f"api/{API_VERSION}/auth/logout/", LogoutView.as_view()),
    path(f"api/{API_VERSION}/auth/confirmation/", email_confirmation),
    
    path("", include("apps.django.core.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += data_patterns
urlpatterns += relation_patterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
