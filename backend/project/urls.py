import private_storage.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.authentication.views import (
    email_confirmation, LoginView, LogoutView, PasswordChangeView, RegisterView, StudentView, UserPaymentViewSet,
)
from apps.event.views import ClasstestViewSet, EventUserRelationViewSet, EventViewSet, ModificationViewSet
from apps.homework.views import (
    HomeworkViewSet, MaterialViewSet, SubmissionViewSet, UserHomeworkRelationViewSet,
)
from apps.lesson.views import CourseViewSet, LessonViewSet, UserLessonRelationViewSet
from apps.news.views import NewsViewSet
from apps.school_data.views import RoomViewSet, SubjectViewSet, TeacherViewSet, UserSubjectRelationViewSet

API_VERSION = "1.0"

router = DefaultRouter()
router.register("lesson", LessonViewSet, basename="Lesson")
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
router.register("material", MaterialViewSet, basename="Material")
router.register("submission", SubmissionViewSet, basename="Submission")

user_relation_router = DefaultRouter()

user_relation_router.register("lesson", UserLessonRelationViewSet, basename="UserLessonRelation")
user_relation_router.register("homework", UserHomeworkRelationViewSet, basename="UserHomeworkRelation")
user_relation_router.register("event", EventUserRelationViewSet, basename="EventUserRelation")
user_relation_router.register("subject", UserSubjectRelationViewSet, basename="UserSubjectRelation")

urlpatterns = [
                  # Static access
                  path("private-media/", include(private_storage.urls)),
    
                  path(f"api/{API_VERSION}/user-relation/", include(user_relation_router.urls)),
                  path(f"api/{API_VERSION}/data/", include(router.urls)),
                  path(f"api/{API_VERSION}/data/", include("rest_framework.urls")),
    
                  path(f"api/{API_VERSION}/auth/change-password/", PasswordChangeView.as_view()),
                  path(f"api/{API_VERSION}/auth/registration/", RegisterView.as_view()),
                  path(f"api/{API_VERSION}/auth/student/", StudentView.as_view()),
                  path(f"api/{API_VERSION}/auth/login/", LoginView.as_view()),
                  path(f"api/{API_VERSION}/auth/logout/", LogoutView.as_view()),
                  path(f"api/{API_VERSION}/auth/confirmation/", email_confirmation),
    
                  path("", include("apps.main.urls")),
                  path("admin/", admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
