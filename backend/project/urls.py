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
from apps.django.main.day.views import (
    get_page_title_view, student_daily_data_view, student_lesson_view, student_week_view, teacher_lesson_view,
    teacher_week_view, teacher_daily_data_view,
)
from apps.django.main.event import routers as event_routers
from apps.django.main.homework import routers as homework_routers
from apps.django.main.homework.views import HomeworkAutocompleteView
from apps.django.main.timetable import routers as timetable_routers
from apps.django.utils.urls import build_patterns


def build_url(prefix: str) -> str:
    return f"api/{prefix}/"


auth_patterns = build_patterns("auth", [
    sessions_routers.auth_router.urls,
])

student_patterns = build_patterns("student", [
    homework_routers.student_router.urls,
    course_routers.student_router.urls,
    homework_routers.student_router.urls,
    poll_routers.student_router.urls,
    event_routers.student_router.urls,
    timetable_routers.student_router.urls,
    user_routers.student_router.urls,
])

teacher_patterns = build_patterns("teacher", [
    homework_routers.teacher_router.urls,
    course_routers.teacher_router.urls,
    homework_routers.teacher_router.urls,
    poll_routers.teacher_router.urls,
    event_routers.teacher_router.urls,
    timetable_routers.teacher_router.urls,
    user_routers.teacher_router.urls,
])

relation_patterns = build_patterns("user-relation", [
    course_routers.relation_router.urls,
    homework_routers.relation_router.urls,
])

urlpatterns = [
    # Static access
    path("private-media/", include(private_storage.urls)),

    # API
    path("api/data/", include("rest_framework.urls")),
    path("api/data/get-page-title/", get_page_title_view),
    path("api/student/contacts/", contacts),
    # path("api/data/timetable/", timetable),
    # path("api/data/daily-data/", daily_data),

    # Student
    path("api/student/daily-data/", student_daily_data_view),
    path("api/student/week/", student_week_view),
    path("api/student/lesson/", student_lesson_view),
    # Teacher
    path("api/teacher/daily-data/", teacher_daily_data_view),
    path("api/teacher/week/", teacher_week_view),
    path("api/teacher/lesson/", teacher_lesson_view),

    # Autocomplete
    path("api/autocomplete/homework/type/", HomeworkAutocompleteView.as_view()),
    # path("api/autocomplete/absence/reason/", AbsenceReasonAutocompleteView.as_view()),

    # Auth
    path("api/auth/change-password/", PasswordChangeView.as_view()),
    path("api/auth/login/", LoginView.as_view()),
    path("api/auth/logout/", LogoutView.as_view()),
    path("api/auth/reset-password/", include("django_rest_passwordreset.urls", namespace="password_reset")),

    path("admin/", admin.site.urls),
    path("", include("user_sessions.urls", "user_sessions")),
    path("api/fcm/devices/", FCMDeviceAuthorizedViewSet.as_view({"post": "create"}), name="create_fcm_device"),
]

urlpatterns += auth_patterns
urlpatterns += relation_patterns
urlpatterns += student_patterns
urlpatterns += teacher_patterns
