from datetime import date, timedelta
from typing import *

from apps.django.extra.scooso_scraper.scrapers.timetable import TimetableRequest
from apps.utils import find_next_date_by_weekday

if TYPE_CHECKING:
    from apps.django.main.lesson.models import Lesson
    from apps.django.extra.scooso_scraper.scrapers.parsers import PureTimetableParserDataType
    from apps.django.main.authentication.models import User, ScoosoData

__all__ = [
    "fetch_timetable", "yield_lessons_with_materials"
]


def yield_lessons_with_materials(
        timetable: "PureTimetableParserDataType",
        lessons: List["Lesson"]
) -> Generator["Lesson", None, None]:
    material_time_ids = [
        material['material']['time_id']
        for material in timetable['materials_data']
    ]
    lesson_time_ids_with_materials = [
        lesson['lesson']['time_id']
        for lesson in timetable['lessons']
        if lesson['lesson']['time_id'] in material_time_ids
    ]
    
    for lesson in lessons:
        if lesson.lessonscoosodata.time_id in lesson_time_ids_with_materials:
            yield lesson


def fetch_timetable(user: "User") -> None:
    next_monday = find_next_date_by_weekday(date.today() - timedelta(days=6), weekday=0)
    scooso_data: "ScoosoData" = user.scoosodata
    
    login_data = {
        "username": scooso_data.username,
        "password": scooso_data.password
    }
    start_dates = [
        next_monday,
        next_monday + timedelta(days=7),
        next_monday + timedelta(days=14),
        next_monday + timedelta(days=21)
    ]
    
    with TimetableRequest(**login_data) as scraper:
        for start_date in start_dates:
            end_date = start_date + timedelta(days=5)
            
            data = scraper.get_timetable(start_date, end_date)
            lessons = scraper.import_timetable_from_scraper(data, [user])
            
            for lesson in yield_lessons_with_materials(data, lessons):
                try:
                    scraper.import_materials_from_lesson(lesson)
                except Exception:
                    continue
