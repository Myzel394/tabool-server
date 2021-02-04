import random

from apps.django.authentication.user.mixins import UserTestMixin
from apps.django.main.course.models import Course
from apps.django.utils.tests_mixins import joinkwargs
from .room import RoomTestMixin
from .subject import SubjectTestMixin


class CourseTestMixin(RoomTestMixin, SubjectTestMixin, UserTestMixin):
    @classmethod
    def Create_course(cls, **kwargs) -> Course:
        participants = kwargs.pop("participants", [])
        
        course = Course.objects.create(
            **joinkwargs({
                "teacher": cls.Create_teacher,
                "subject": cls.Create_subject,
                "course_number": lambda: random.randint(1, 5)
            }, kwargs)
        )
        course.participants.add(*participants)
        
        return course
