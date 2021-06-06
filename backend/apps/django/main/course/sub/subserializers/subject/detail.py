from rest_framework import serializers

from apps.django.main.course import constants
from apps.django.main.course.models import Subject
from apps.django.utils.serializers import UserRelationField
from .relation import UserSubjectRelationSerializer

__all__ = [
    "DetailSubjectSerializer"
]


class DetailSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "name", "short_name", "id", "user_relation"
        ]
        read_only = [
            "id", "user_relation"
        ]

    user_relation = UserRelationField(
        UserSubjectRelationSerializer,
        default=lambda subject, _: {
            "color": constants.SUBJECT_COLORS_MAPPING.get(
                subject.name.lower(), "#232323"
            )
        }
    )
