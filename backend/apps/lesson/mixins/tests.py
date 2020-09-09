import random
from abc import ABC
from datetime import datetime, time, timedelta
from typing import List, Optional

from dateutil.rrule import MINUTELY, rrule

from apps.lesson.models import Lesson
from apps.timetable.mixins.tests import RoomTestMixin, SubjectTestMixin, TeacherTestMixin
from apps.utils.fields.weekday import WeekdayChoices
from apps.utils.tests import StartTimeEndTimeTestMixin
from apps.utils.time import dummy_datetime_from_time


class RandomLessonTextMixin(
    TeacherTestMixin,
    SubjectTestMixin,
    RoomTestMixin,
    StartTimeEndTimeTestMixin,
    ABC
):
    @classmethod
    def Create_lesson(cls, **kwargs) -> Lesson:
        return Lesson.objects.create(
            **{
                "teacher": cls.Create_teacher(),
                "room": cls.Create_room(),
                "subject": cls.Create_subject(),
                "start_time": cls.start_time(),
                "end_time": cls.end_time(),
                "weekday": random.choice(WeekdayChoices.values),
                **kwargs
            }
        )
    
    @classmethod
    def Create_lessons(
            cls,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            duration: int = 45,
            **kwargs
    ) -> List[Lesson]:
        start_time = start_time or time(hour=7, minute=55)
        end_time = end_time or (dummy_datetime_from_time(time(hour=13, minute=10)) - timedelta(minutes=duration)).time()
        
        lessons = []
        
        for weekday in WeekdayChoices.values:
            for current_time in rrule(
                    MINUTELY,
                    interval=duration,
                    dtstart=dummy_datetime_from_time(start_time),
                    until=dummy_datetime_from_time(end_time)
            ):
                lesson = cls.Create_lesson(
                    **{
                        "start_time": current_time,
                        "end_time": (dummy_datetime_from_time(current_time) + timedelta(minutes=duration)).time(),
                        "weekday": weekday,
                        **kwargs
                    }
                )
                lessons.append(lesson)
        
        return lessons
