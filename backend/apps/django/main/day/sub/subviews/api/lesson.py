from datetime import date
from typing import *

from django_hint import RequestType
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from apps.django.main.event.models import Modification
from apps.django.main.event.serializers import StudentDetailModificationSerializer, TeacherDetailModificationSerializer
from apps.django.main.homework.models import Classbook, Homework, Material, Submission
from apps.django.main.homework.serializers import (
    StudentDetailClassbookSerializer, StudentDetailHomeworkSerializer,
    StudentDetailMaterialSerializer, StudentDetailSubmissionSerializer, TeacherDetailClassbookSerializer,
    TeacherDetailHomeworkSerializer, TeacherDetailMaterialSerializer, TeacherDetailSubmissionSerializer,
)
from apps.django.main.timetable.mixins import get_via_referenced_lesson_date
from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsStudent, IsTeacher
from ....serializers import LessonViewSerializer
from ....throttles import LessonViewThrottle

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User
    from apps.django.main.timetable.models import Lesson

__all__ = [
    "student_lesson_view", "teacher_lesson_view"
]


def parse_serializer(data: dict, serializer_context: dict) -> tuple["Lesson", date]:
    serializer = LessonViewSerializer(data=data, context=serializer_context)
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
        "lesson": lesson,
        "classbook": classbook,
        "materials": materials,
        "submissions": submissions,
        "modifications": modifications,
        "homeworks": homeworks
    }


@api_view(["GET"])
@throttle_classes([LessonViewThrottle])
@permission_classes([AuthenticationAndActivePermission & IsStudent])
def student_lesson_view(request: RequestType):
    serializer_context = {
        "request": request
    }
    lesson_args = parse_serializer(request.GET, serializer_context)
    user = request.user
    elements = get_elements(user, *lesson_args)
    
    return Response({
        "classbook": StudentDetailClassbookSerializer(instance=elements["classbook"], context=serializer_context).data,
        "materials": StudentDetailMaterialSerializer(
            instance=elements["materials"],
            many=True,
            context=serializer_context
        ).data,
        "submissions": StudentDetailSubmissionSerializer(
            instance=elements["submissions"],
            many=True,
            context=serializer_context
        ).data,
        "modifications": StudentDetailModificationSerializer(
            instance=elements["modifications"],
            many=True,
            context=serializer_context
        ).data,
        "homeworks": StudentDetailHomeworkSerializer(
            instance=elements["homeworks"],
            many=True,
            context=serializer_context
        ).data,
        "lesson_information": StudentDetailLessonSerializer(
            instance=elements["lesson"],
            context=serializer_context
        ).data
    })


@api_view(["GET"])
@throttle_classes([LessonViewThrottle])
@permission_classes([AuthenticationAndActivePermission & IsTeacher])
def teacher_lesson_view(request: RequestType):
    serializer_context = {
        "request": request
    }
    lesson_args = parse_serializer(request.GET, serializer_context)
    user = request.user
    elements = get_elements(user, *lesson_args)
    
    return Response({
        "classbook": TeacherDetailClassbookSerializer(instance=elements["classbook"], context=serializer_context).data,
        "materials": TeacherDetailMaterialSerializer(
            instance=elements["materials"],
            many=True,
            context=serializer_context
        ).data,
        "submissions": TeacherDetailSubmissionSerializer(
            instance=elements["submissions"],
            many=True,
            context=serializer_context
        ).data,
        "modifications": TeacherDetailModificationSerializer(
            instance=elements["modifications"],
            many=True,
            context=serializer_context
        ).data,
        "homeworks": TeacherDetailHomeworkSerializer(
            instance=elements["homeworks"],
            many=True,
            context=serializer_context
        ).data,
        "lesson_information": TeacherDetailLessonSerializer(
            instance=elements["lesson"],
            context=serializer_context
        ).data
    })
