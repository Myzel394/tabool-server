from rest_framework import serializers

from ....models import Course

__all__ = [
    "BaseCourseSerializer", "ParticipantsCountMixin"
]


class BaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course


class ParticipantsCountMixin(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()
    
    @staticmethod
    def get_participants_count(obj: Course):
        return obj.participants.all().count()
