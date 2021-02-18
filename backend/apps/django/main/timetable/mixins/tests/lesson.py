import random
from datetime import date
from typing import *

from apps.django.main.course.mixins import CourseTestMixin, joinkwargs
from apps.django.main.timetable.models import Lesson, Timetable
from apps.utils import find_next_date_by_weekday
from .timetable import TimetableTestMixin


class LessonTestMixin(TimetableTestMixin, CourseTestMixin):
    associated_timetable: Optional[Timetable]
    
    @classmethod
    def Create_lesson_argument(cls, lesson: Optional[Lesson] = None, lesson_date: Optional[date] = None):
        lesson = lesson or cls.Create_lesson()
        
        return {
            "lesson": lambda: lesson,
            "lesson_date": lambda: lesson_date or find_next_date_by_weekday(date.today(), lesson.weekday)
        }
    
    @classmethod
    def get_lesson_argument(cls, lesson: Optional[Lesson] = None, lesson_date: Optional[date] = None) -> dict:
        lesson = lesson or cls.Create_lesson()
        
        return {
            "lesson": lesson.id,
            "lesson_date": lesson_date or find_next_date_by_weekday(date.today(), lesson.weekday)
        }
    
    @classmethod
    def Create_lesson(cls, **kwargs) -> Lesson:
        return Lesson.objects.create(
            **joinkwargs({
                "timetable": lambda: getattr(cls, "associated_timetable", cls.Create_timetable()),
                "course": cls.Create_course,
                "weekday": lambda: random.randint(0, 4),
                "start_hour": lambda: random.randint(1, 5),
                "end_hour": lambda: random.randint(5, 10),
            }, kwargs)
        )
    
    @classmethod
    def Create_whole_timetable(cls, **kwargs) -> Timetable:
        timetable = cls.Create_timetable(**kwargs)
        cls.associated_timetable = timetable
        
        for weekday in range(1, 5 + 1):
            for hour in range(1, 6, 2):
                cls.Create_lesson(
                    timetable=timetable,
                    weekday=weekday,
                    start_hour=hour,
                    end_hour=hour,
                )
        
        return timetable
