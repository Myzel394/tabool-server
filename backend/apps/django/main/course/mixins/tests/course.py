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
        teacher = kwargs.pop("teacher", None)
        
        if associated_teacher := getattr(cls, "associated_teacher", None):
            teacher = associated_teacher.teacher
        
        course = Course.objects.create(
            **joinkwargs({
                "teacher": lambda: teacher or cls.Create_teacher(),
                "subject": cls.Create_subject,
                "course_number": lambda: random.randint(1, 5),
                "room": cls.Create_room
            }, kwargs)
        )
        course.participants.add(
            *participants,
        )
        
        if hasattr(cls, "associated_student"):
            course.participants.add(cls.associated_student.student)
        
        return course
