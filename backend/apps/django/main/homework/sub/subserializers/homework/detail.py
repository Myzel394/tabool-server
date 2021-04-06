from typing import *

from rest_framework import serializers

from apps.django.authentication.user.sub.subserializers.student import DetailStudentSerializer
from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from apps.django.utils.serializers import UserRelationField
from .base import BaseHomeworkSerializer
from ..user_relations import UserHomeworkRelationSerializer
from ....models import UserHomeworkRelation

if TYPE_CHECKING:
    from ....models import Homework

__all__ = [
    "StudentDetailHomeworkSerializer", "TeacherDetailHomeworkSerializer"
]


class StudentDetailHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "information", "type", "created_at", "id",
            "user_relation", "is_private"
        ]

    lesson = StudentDetailLessonSerializer()

    user_relation = UserRelationField(
        UserHomeworkRelationSerializer,
        default={
            "completed": False,
            "ignored": False
        }
    )


class TeacherDetailHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "information", "type", "created_at", "id",
            "private_to_student",

            "completed_amount",
            "ignored_amount"
        ]

    lesson = TeacherDetailLessonSerializer()
    private_to_student = DetailStudentSerializer()

    completed_amount = serializers.SerializerMethodField()
    ignored_amount = serializers.SerializerMethodField()

    @staticmethod
    def get_completed_amount(instance: "Homework") -> int:
        return UserHomeworkRelation.objects \
            .all() \
            .only("homework", "completed") \
            .filter(homework=instance, completed=True) \
            .count()

    @staticmethod
    def get_ignored_amount(instance: "Homework") -> int:
        return UserHomeworkRelation.objects \
            .all() \
            .only("homework", "ignored") \
            .filter(homework=instance, ignored=True) \
            .count()
