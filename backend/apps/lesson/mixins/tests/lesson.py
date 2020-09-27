import random
from datetime import datetime, time, timedelta
from typing import *

from dateutil.rrule import MINUTELY, rrule

from apps.utils.tests import joinkwargs, StartTimeEndTimeTestMixin
from apps.utils.time import dummy_datetime_from_target
from constants.weekdays import ALLOWED_WEEKDAYS
from .course import CourseTestMixin
from .room import RoomTestMixin
from ...models import Lesson, LessonData

__all__ = [
    "LessonTestMixin"
]


class LessonTestMixin(
    RoomTestMixin,
    StartTimeEndTimeTestMixin,
    CourseTestMixin
):
    @classmethod
    def Create_lesson(cls, **kwargs):
        return Lesson.objects.create_automatically(
            **joinkwargs(
                {
                    "lesson_data": cls.Create_lesson_data,
                },
                kwargs
            )
        )
    
    @classmethod
    def Create_lesson_data(cls, **kwargs) -> LessonData:
        return LessonData.objects.create(
            **joinkwargs(
                {
                    "room": cls.Create_room,
                    "course": cls.Create_course,
                    "start_time": cls.start_time,
                    "end_time": cls.end_time,
                    "weekday": lambda: random.choice([x[0] for x in ALLOWED_WEEKDAYS]),
                },
                kwargs
            )
        )
    
    @classmethod
    def Create_lessons_data(
            cls,
            start_time: Optional[time] = None,
            end_time: Optional[time] = None,
            duration: int = 45,
            **kwargs
    ) -> List[LessonData]:
        start_time = start_time or time(hour=7, minute=55)
        end_time = end_time or (
                    dummy_datetime_from_target(time(hour=13, minute=10)) - timedelta(minutes=duration)).time()
        
        lessons = []
        
        weekday: int
        for weekday in [x[0] for x in ALLOWED_WEEKDAYS]:
            current_time: datetime
            for current_time in rrule(
                    MINUTELY,
                    interval=duration,
                    dtstart=dummy_datetime_from_target(start_time),
                    until=dummy_datetime_from_target(end_time)
            ):
                lesson = cls.Create_lesson_data(
                    **joinkwargs(
                        {
                            "start_time": lambda: current_time.time(),
                            "end_time": lambda: (current_time + timedelta(minutes=duration)).time(),
                            "weekday": lambda: weekday,
                        },
                        kwargs
                    )
                )
                lessons.append(lesson)
        
        return lessons
