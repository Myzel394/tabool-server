from apps.utils.tests import joinkwargs
from .teacher import TeacherTestMixin
from .subject import SubjectTestMixin
from ...models.course import Course


__all__ = [
    "CourseTestMixin"
]


class CourseTestMixin(TeacherTestMixin, SubjectTestMixin):
    @classmethod
    def Create_course(cls, **kwargs):
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
