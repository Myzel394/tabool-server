import random
from typing import *

from apps.django.main.course.mixins import CourseTestMixin, joinkwargs
from apps.django.main.timetable.models import Lesson, Timetable
from .timetable import TimetableTestMixin


class LessonTestMixin(TimetableTestMixin, CourseTestMixin):
    associated_timetable: Optional[Timetable]
    
    @classmethod
    def Create_lesson(cls, **kwargs) -> Lesson:
        return Lesson.objects.create(
            **joinkwargs({
                "timetable": lambda: cls.associated_timetable or cls.Create_timetable(),
                "course": cls.Create_course,
                "start_hour": lambda: random.randint(1, 13),
                "end_hour": lambda: random.randint(1, 13),
            }, kwargs)
        )
    
    @classmethod
    def Create_whole_timetable(cls) -> Timetable:
        timetable = cls.Create_timetable()
        
        for weekday in range(1, 5 + 1):
            for hour in range(1, 5):
                cls.Create_lesson(
                    timetable=timetable,
                    weekday=weekday,
                    start_hour=hour,
                    end_hour=hour,
                )
        
        return timetable
