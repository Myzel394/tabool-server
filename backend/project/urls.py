import private_storage.urls
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.authentication.views import (
    LoginView, LogoutView, PasswordChangeView, RegisterView, StudentView,
    UserPaymentViewSet,
)
from apps.event.views import ClasstestViewSet, EventUserRelationViewSet, EventViewSet, ModificationViewSet
from apps.homework.views import HomeworkViewSet, MaterialDownloadView, UserHomeworkRelationViewSet
from apps.lesson.views import (
    CourseViewSet, RoomViewSet, SubjectViewSet, TeacherViewSet, UserLessonRelationViewSet,
    UserSubjectRelationViewSet,
)
from apps.news.views import NewsViewSet
from apps.timetable.views import TimetableViewSet

router = DefaultRouter()
router.register("timetable", TimetableViewSet, basename="Timetable")
router.register("homework", HomeworkViewSet, basename="Homework")
router.register("modification", ModificationViewSet, basename="Modification")
router.register("classtest", ClasstestViewSet, basename="Classtest")
router.register("event", EventViewSet, basename="Event")
router.register("course", CourseViewSet, basename="Course")
router.register("room", RoomViewSet, basename="Room")
router.register("subject", SubjectViewSet, basename="Subject")
router.register("teacher", TeacherViewSet, basename="Teacher")
router.register("news", NewsViewSet, basename="News")
router.register("user-payment", UserPaymentViewSet, basename="PaidUser")

# TODO: Add user uploads & downloads
router.register("user-relation/lesson", UserLessonRelationViewSet, basename="UserLessonRelation")
router.register("user-relation/homework", UserHomeworkRelationViewSet, basename="UserHomeworkRelation")
router.register("user-relation/event", EventUserRelationViewSet, basename="EventUserRelation")
router.register("user-relation/subject", UserSubjectRelationViewSet, basename="UserSubjectRelation")

urlpatterns = [
    # Static access
    path("private-media/", MaterialDownloadView.as_view()),
    path("private-media/", include(private_storage.urls)),
    
    path("api/", include(router.urls)),
    path("api/", include("rest_framework.urls")),
    
    path("api/auth/change-password/", PasswordChangeView.as_view()),
    path("api/auth/registration/", RegisterView.as_view()),
    path("api/auth/student/", StudentView.as_view()),
    path("api/auth/login/", LoginView.as_view()),
    path("api/auth/logout/", LogoutView.as_view()),
    
    path("", include("apps.main.urls")),
    path("admin/", admin.site.urls),

]
