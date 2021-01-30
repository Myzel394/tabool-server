from typing import *

from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Modification

if TYPE_CHECKING:
    from apps.django.main.lesson.models import Lesson
    from apps.django.main.school_data.models import Room, Teacher, Subject

__all__ = [
    "ModificationScoosoScraperSerializer"
]


class ModificationScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "information", "modification_type", "start_datetime", "end_datetime"
        ]
    
    def create(self, validated_data):
        lesson: "Lesson" = validated_data.get("lesson")
        new_room: "Room" = validated_data.pop("new_room", None)
        new_teacher: "Teacher" = validated_data.pop("new_teacher", None)
        new_subject: "Subject" = validated_data.pop("new_subject", None)
        
        unique_data = {
            "lesson": validated_data.pop("lesson"),
            "start_datetime": validated_data.pop("start_datetime"),
            "end_datetime": validated_data.pop("end_datetime"),
        }
        other_data = {
            key: value
            for key, value in validated_data.items()
            if key not in unique_data
        }
        
        # Make sure new data is not the same as the old one
        if new_subject != lesson.course.subject:
            other_data["new_subject"] = new_subject
        if new_room != lesson.room:
            other_data["new_room"] = new_room
        if new_teacher != lesson.course.teacher:
            other_data["new_teacher"] = new_teacher
        
        # Create instance
        instance, _ = Modification.objects.get_or_create(**unique_data)
        
        for key, value in other_data.items():
            setattr(instance, key, value)
        
        instance.save()
        
        return instance
