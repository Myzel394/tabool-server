from apps.relation_managers.managers import SimpleRelatedRelationManagerMixin
from ...models import Course, Lesson

__all__ = [
    "LessonCourseRelationManager"
]


class LessonCourseRelationManager(SimpleRelatedRelationManagerMixin):
    class Meta:
        model = Course
    
    related_model = Lesson
    
    def get_users(self):
        return self.instance.participants.all()
    
    @staticmethod
    def get_model_from_related_instance(instance: Lesson) -> Course:
        return instance.lesson_data.course
