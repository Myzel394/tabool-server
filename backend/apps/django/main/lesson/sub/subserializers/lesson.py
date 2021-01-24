from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.django.main.event.models import Modification
from apps.django.main.event.sub.subserializers.modification import ModificationDetailSerializer
from apps.django.main.homework.models import Homework, Material, Submission
from apps.django.main.homework.sub.subserializers.homework import HomeworkDetailSerializer
from apps.django.main.homework.sub.subserializers.material import MaterialDetailSerializer
from apps.django.main.homework.sub.subserializers.submission import SubmissionDetailSerializer
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from .classbook import ClassbookDetailSerializer
from .lesson_data import LessonDataDetailSerializer, LessonDataListSerializer
from ...models import Lesson, LessonAbsence

__all__ = [
    "LessonListSerializer", "LessonDetailSerializer", "LessonDetailSerializer", "LessonDetailEndpointSerializer",
]


class LessonListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "has_video_conference", "id"
        ]
    
    lesson_data = LessonDataListSerializer()
    
    has_video_conference = serializers.SerializerMethodField()
    
    def get_has_video_conference(self, instance: Lesson) -> str:
        return instance.video_conference_link is not None


class LessonDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id", "absence", "classbook", "materials", "homeworks", "modifications",
            "submissions", "video_conference_link"
        ]
    
    lesson_data = LessonDataDetailSerializer()
    classbook = ClassbookDetailSerializer()
    
    absence = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    homeworks = serializers.SerializerMethodField()
    modifications = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    
    def get_absence(self, instance: Lesson):
        from .lesson_absence import DetailLessonAbsenceSerializer
        user = self.context["request"].user
        
        try:
            absence = LessonAbsence.objects \
                .only("associated_user", "lesson") \
                .get(associated_user=user, lesson=instance)
        except ObjectDoesNotExist:
            return None
        
        return DetailLessonAbsenceSerializer(instance=absence).data
    
    def get_materials(self, instance: Lesson):
        materials = Material.objects.only("lesson").filter(lesson=instance)
        
        return MaterialDetailSerializer(materials, many=True, context=self.context).data
    
    def get_homeworks(self, instance: Lesson):
        homeworks = Homework.objects.only("lesson").filter(lesson=instance).not_old()
        
        return HomeworkDetailSerializer(homeworks, many=True, context=self.context).data
    
    def get_modifications(self, instance: Lesson):
        modifications = Modification.objects.only("lesson").filter(lesson=instance)
        
        return ModificationDetailSerializer(modifications, many=True, context=self.context).data
    
    def get_submissions(self, instance: Lesson):
        submissions = Submission.objects \
            .user_accessible(self.context["request"].user) \
            .only("lesson") \
            .filter(lesson=instance)
        
        return SubmissionDetailSerializer(submissions, many=True, context=self.context).data


class LessonDetailEndpointSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "classbook", "date", "id"
        ]
    
    classbook = ClassbookDetailSerializer()
    lesson_data = LessonDataDetailSerializer()
