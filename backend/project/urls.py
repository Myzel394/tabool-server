from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.authentication.views import LoginView, LogoutView, PasswordChangeView, RegisterView
from apps.event.views import ClasstestViewSet, EventViewSet, UserEventRelationViewSet
from apps.homework.views import HomeworkViewSet, UserHomeworkRelationViewSet
from apps.lesson.views import CourseViewSet, RoomViewSet, SubjectViewSet, TeacherViewSet, UserLessonRelationViewSet
from apps.news.views import NewsViewSet
from apps.timetable.views import TimetableViewSet

router = DefaultRouter()
router.register("timetable", TimetableViewSet, basename="Timetable")
router.register("homework", HomeworkViewSet, basename="Homework")
router.register("classtest", ClasstestViewSet, basename="Classtest")
router.register("event", EventViewSet, basename="Event")
router.register("course", CourseViewSet, basename="Course")
router.register("room", RoomViewSet, basename="Room")
router.register("subject", SubjectViewSet, basename="Subject")
router.register("teacher", TeacherViewSet, basename="Teacher")
router.register("news", NewsViewSet, basename="News")

router.register("lesson/user-relation", UserLessonRelationViewSet, basename="UserLessonRelation")
router.register("homework/user-relation", UserHomeworkRelationViewSet, basename="UserHomeworkRelation")
router.register("event/user-relation", UserEventRelationViewSet, basename="UserEventRelation")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("rest_framework.urls")),
    path("", include("apps.main.urls")),
    
    path("api/change-password/", PasswordChangeView.as_view()),
    path("api/registration/", RegisterView.as_view()),
    path("api/login/", LoginView.as_view()),
    path("api/logout/", LogoutView.as_view()),
]
