from apps.homework.models import Homework
from apps.lesson.models import Course
from apps.lesson.sub.subrelation_managers import LessonCourseRelationManager

__all__ = [
    "HomeworkCourseRelationManager"
]


class HomeworkCourseRelationManager(LessonCourseRelationManager):
    class Meta:
        model = Course
    
    related_model = Homework
    
    def get_users(self):
        return self.instance.participants.all()
