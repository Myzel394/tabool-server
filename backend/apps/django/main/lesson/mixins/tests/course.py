from apps.django.main.school_data.mixins.tests import *
from apps.django.main.school_data.mixins.tests.teacher import TeacherTestMixin
from apps.django.utils.tests import joinkwargs
from ...models.course import Course

__all__ = [
    "CourseTestMixin"
]


class CourseTestMixin(TeacherTestMixin, SubjectTestMixin):
    @classmethod
    def Create_course(cls, **kwargs) -> Course:
        course = Course.objects.create(
            **joinkwargs(
                {
                    "subject": cls.Create_subject,
                    "teacher": cls.Create_teacher
                },
                kwargs
            )
        )
        
        if value := getattr(cls, "associated_user", None):
            course.participants.add(value)
            course.save()
        
        return course
