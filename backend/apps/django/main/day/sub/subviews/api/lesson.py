from datetime import date
from typing import *

from django_hint import RequestType
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response

from apps.django.main.event.models import Modification
from apps.django.main.event.sub.subserializers.modification import DetailModificationSerializer
from apps.django.main.homework.models import Classbook, Homework, Material, Submission
from apps.django.main.homework.sub.subserializers.classbook import DetailClassbookSerializer
from apps.django.main.homework.sub.subserializers.homework import (
    StudentDetailHomeworkSerializer,
    TeacherDetailHomeworkSerializer,
)
from apps.django.main.homework.sub.subserializers.material import DetailMaterialSerializer
from apps.django.main.homework.sub.subserializers.submission import DetailSubmissionSerializer
from apps.django.main.timetable.mixins import get_via_referenced_lesson_date
from ....serializers import LessonViewSerializer
from ....throttles import LessonViewThrottle

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User
    from apps.django.main.timetable.models import Lesson

__all__ = [
    "student_lesson_view", "teacher_lesson_view"
]


def parse_serializer(data: dict) -> tuple["Lesson", date]:
    serializer = LessonViewSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    
    validated_data = serializer.validated_data
    lesson = validated_data["lesson"]
    lesson_date = validated_data["lesson_date"]
    
    return lesson, lesson_date


def get_elements(user: "User", lesson: "Lesson", lesson_date: date) -> dict:
    lesson_args = lesson, lesson_date
    
    classbook = get_via_referenced_lesson_date(Classbook.objects.from_user(user), *lesson_args)
    materials = get_via_referenced_lesson_date(Material.objects.from_user(user), many=True, *lesson_args)
    submissions = get_via_referenced_lesson_date(Submission.objects.from_user(user), many=True, *lesson_args)
    modifications = get_via_referenced_lesson_date(Modification.objects.from_user(user), many=True, *lesson_args)
    homeworks = get_via_referenced_lesson_date(Homework.objects.from_user(user), many=True, *lesson_args)
    
    return {
        "classbook": classbook,
        "materials": materials,
        "submissions": submissions,
        "modifications": modifications,
        "homeworks": homeworks
    }


@api_view(["GET"])
@throttle_classes([LessonViewThrottle])
def student_lesson_view(request: RequestType):
    lesson_args = parse_serializer(request.data)
    user = request.user
    serializer_context = {
        "request": request
    }
    elements = get_elements(user=user, *lesson_args)
    
    return Response({
        "classbook": DetailClassbookSerializer(instance=elements["classbook"], context=serializer_context).data,
        "materials": DetailMaterialSerializer(instance=elements["materials"], context=serializer_context).data,
        "submissions": DetailSubmissionSerializer(instance=elements["submissions"], context=serializer_context).data,
        "modifications": DetailModificationSerializer(
            instance=elements["modifications"],
            context=serializer_context
        ).data,
        "homeworks": StudentDetailHomeworkSerializer(instance=elements["homeworks"], context=serializer_context).data,
    })


@api_view(["GET"])
@throttle_classes([LessonViewThrottle])
def teacher_lesson_view(request: RequestType):
    lesson_args = parse_serializer(request.data)
    user = request.user
    serializer_context = {
        "request": request
    }
    elements = get_elements(user=user, *lesson_args)
    
    return {
        "classbook": DetailClassbookSerializer(instance=elements["classbook"], context=serializer_context).data,
        "materials": DetailMaterialSerializer(instance=elements["materials"], context=serializer_context).data,
        "submissions": DetailSubmissionSerializer(instance=elements["submissions"], context=serializer_context).data,
        "modifications": DetailModificationSerializer(
            instance=elements["modifications"],
            context=serializer_context
        ).data,
        "homeworks": TeacherDetailHomeworkSerializer(instance=elements["homeworks"], context=serializer_context).data,
    }
