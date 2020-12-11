from django.db.models import Count, Q, Sum
from django_hint import RequestType
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.django.main.event.models import Modification
from apps.django.main.event.options import ModificationTypeOptions
from apps.django.main.lesson.models import Lesson, LessonData
from apps.django.utils.viewsets import RetrieveAllMixin
from ...models import Teacher
from ...paginations import LargeSetPagination
from ...serializers import TeacherDetailSerializer, TeacherListSerializer

__all__ = [
    "TeacherViewSet"
]


class TeacherViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["last_name", "short_name"]
    model = Teacher
    pagination_class = LargeSetPagination
    permission_classes = [IsAuthenticated]  # Teachers must be collected for full registration
    ordering_fields = ["last_name", "short_name"]
    
    def get_serializer_class(self):
        if self.action == "list":
            return TeacherListSerializer
        return TeacherDetailSerializer
    
    @action(url_path="information", detail=True, methods=["GET"])
    def information(self, request: RequestType, pk: str = None):
        teacher = get_object_or_404(Teacher, id=pk)
        user_lessons = Lesson.objects.from_user(request.user)
        missing_modifications = Modification.objects.filter(
            Q(modification_type=ModificationTypeOptions.FREE_PERIOD) |
            Q(modification_type=ModificationTypeOptions.SELF_LEARN) |
            Q(modification_type=ModificationTypeOptions.REPLACEMENT)
        ).distinct()
        missing_ratio = (
                (
                    missing_modifications
                        .only("lesson")
                        .filter(lesson__in=user_lessons.filter(lesson_data__course__teacher=teacher).distinct())
                        .distinct()
                        .count()
                ) /
                (
                    user_lessons
                        .filter(lesson_data__course__teacher=teacher)
                        .distinct()
                        .count()
                )
        )
        teacher_missing_ratio = (
                (
                    missing_modifications
                        .filter(lesson__lesson_data__course__teacher=teacher)
                        .distinct()
                        .count()
                ) /
                (
                    Lesson
                        .objects
                        .filter(lesson_data__course__teacher=teacher)
                        .distinct()
                        .count()
                )
        )
        
        return Response({
            "course_count": len(set(
                LessonData.objects
                    .from_user(request.user)
                    .filter(course__teacher=teacher)
                    .values_list("course", flat=True)
            )),
            "teacher_course_count": len(set(
                LessonData.objects
                    .filter(course__teacher=teacher)
                    .values_list("course", flat=True)
            )),
            "teacher_participants_count": (
                LessonData.objects
                    .filter(course__teacher=teacher)
                    .annotate(participants_count=Count("course__participants"))
                    .aggregate(full_count=Sum("participants_count"))["full_count"]
            ),
            "missing_ratio": round(missing_ratio, 2),
            "teacher_missing_ratio": round(teacher_missing_ratio, 2)
        })
