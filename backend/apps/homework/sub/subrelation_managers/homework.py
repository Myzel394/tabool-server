from apps.homework.models import Homework
from apps.lesson.models import Course
from apps.relation_managers.managers import SimpleRelatedRelationManagerMixin

__all__ = [
    "HomeworkCourseRelationManager"
]


class HomeworkCourseRelationManager(SimpleRelatedRelationManagerMixin):
    class Meta:
        model = Course
    
    related_model = Homework
    
    def get_users(self):
        return self.instance.participants.all()
    
    @staticmethod
    def get_model_from_related_instance(instance: Homework) -> Course:
        return instance.lesson.lesson_data.course
