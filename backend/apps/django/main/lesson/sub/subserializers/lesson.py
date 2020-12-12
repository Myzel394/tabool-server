from rest_framework import serializers

from apps.django.main.event.models import Modification
from apps.django.main.event.sub.subserializers.modification import ModificationDetailSerializer
from apps.django.main.homework.models import Homework, Material
from apps.django.main.homework.sub.subserializers.homework import HomeworkDetailSerializer
from apps.django.main.homework.sub.subserializers.material import MaterialDetailSerializer
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin, UserRelationField
from .classbook import ClassbookDetailSerializer
from .lesson_data import LessonDataDetailSerializer, LessonDataListSerializer
from .user_relations import UserLessonRelationSerializer
from ...models import Lesson

__all__ = [
    "LessonListSerializer", "LessonDetailSerializer", "LessonDetailSerializer", "LessonTimetableSerializer"
]


class LessonListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id"
        ]
    
    lesson_data = LessonDataListSerializer()


class LessonDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id", "user_relation", "classbook", "materials", "homeworks", "modifications"
        ]
    
    user_relation = UserRelationField(UserLessonRelationSerializer)
    
    lesson_data = LessonDataDetailSerializer()
    classbook = ClassbookDetailSerializer()
    
    materials = serializers.SerializerMethodField()
    homeworks = serializers.SerializerMethodField()
    modifications = serializers.SerializerMethodField()
    
    def get_materials(self, instance: Lesson):
        materials = Material.objects.only("lesson").filter(lesson=instance)
        
        return MaterialDetailSerializer(materials, many=True, context=self.context).data
    
    def get_homeworks(self, instance: Lesson):
        homeworks = Homework.objects.only("lesson").filter(lesson=instance)
        
        return HomeworkDetailSerializer(homeworks, many=True, context=self.context).data
    
    def get_modifications(self, instance: Lesson):
        modifications = Modification.objects.only("lesson").filter(lesson=instance)
        
        return ModificationDetailSerializer(modifications, many=True, context=self.context).data


class LessonTimetableSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id"
        ]
    
    lesson_data = LessonDataDetailSerializer()
