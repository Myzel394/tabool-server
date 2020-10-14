from apps.lesson.public.serializer_fields import CourseField
from apps.school_data.public.serializer_fields import RoomField
from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Classtest

__all__ = [
    "ClasstestListSerializer", "ClasstestDetailSerializer"
]


class ClasstestListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Classtest
        fields = [
            "course", "targeted_date", "id"
        ]
    
    course = CourseField()


class ClasstestDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Classtest
        fields = [
            "course", "room", "targeted_date", "information", "created_at", "id"
        ]
        read_only_fields = [
            "created_at"
        ]
    
    course = CourseField()
    room = RoomField(required=False)
