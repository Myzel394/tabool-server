from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.django.main.event.models import Modification
from apps.django.main.homework.models import Homework, Material, Submission
from .base import BaseLessonSerializer
from .homework import LessonHomeworkSerializer
from .material import LessonMaterialSerializer
from .modification import LessonModificationSerializer
from .submission import LessonSubmissionSerializer
from ..classbook import ClassbookSerializer
from ..lesson_absence.detail import DetailLessonAbsenceSerializer
from ..lesson_data.detail import DetailLessonDataSerializer
from ....models import Lesson, LessonAbsence

__all__ = [
    "DetailLessonSerializer"
]


class DetailLessonSerializer(BaseLessonSerializer):
    class Meta(BaseLessonSerializer.Meta):
        model = Lesson
        fields = [
            "lesson_data", "date", "id", "absence", "classbook", "materials", "homeworks", "modifications",
            "submissions", "video_conference_link"
        ]
    
    lesson_data = DetailLessonDataSerializer()
    classbook = ClassbookSerializer()
    
    absence = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    homeworks = serializers.SerializerMethodField()
    modifications = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    
    def get_absence(self, instance: Lesson):
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
        
        return LessonMaterialSerializer(materials, many=True, context=self.context).data
    
    def get_homeworks(self, instance: Lesson):
        homeworks = Homework.objects.only("lesson").filter(lesson=instance).not_old()
        
        return LessonHomeworkSerializer(homeworks, many=True, context=self.context).data
    
    def get_modifications(self, instance: Lesson):
        modifications = Modification.objects.only("lesson").filter(lesson=instance)
        
        return LessonModificationSerializer(modifications, many=True, context=self.context).data
    
    def get_submissions(self, instance: Lesson):
        submissions = Submission.objects \
            .user_accessible(self.context["request"].user) \
            .only("lesson") \
            .filter(lesson=instance)
        
        return LessonSubmissionSerializer(submissions, many=True, context=self.context).data
