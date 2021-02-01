import re
from datetime import date, timedelta
from typing import *

from apps.django.main.school_data.models import Teacher
from apps.utils import find_next_date_by_weekday
from .other_scrapers.scrape_teachers import scrape_teachers
from .scrapers.timetable import TimetableRequest

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User, ScoosoData
    from apps.django.main.lesson.models import Lesson

__all__ = [
    "import_teachers", "fetch_timetable"
]

REMOVE_TITLES = [r"Prof\.", r"Dr\.", r"PD"]
REMOVE_TITLES_JOINED = '|'.join(REMOVE_TITLES)

teacher_first_name_regex = re.compile(
    rf"(?:{REMOVE_TITLES_JOINED})? ?(?:{REMOVE_TITLES_JOINED})? ?(?:{REMOVE_TITLES_JOINED})? ?(\w+)")


def get_teacher_first_name(name: str) -> str:
    if match := teacher_first_name_regex.match(name):
        return match.group(1)
    return name


def import_teachers() -> list[Teacher]:
    teachers = scrape_teachers()
    teachers_added = []
    
    for teacher_data in teachers:
        teacher, _ = Teacher.objects.get_or_create(
            short_name=teacher_data['short_name']
        )
        teacher.first_name = get_teacher_first_name(teacher_data['first_name'])
        teacher.last_name = teacher_data['last_name']
        teacher.email = teacher_data['email'].removeprefix("mailto:")
        teacher.gender = teacher_data['gender']
        teacher.save()
        
        teachers_added.append(teacher)
    
    return teachers_added


def fetch_material(lesson: "Lesson", scraper: TimetableRequest) -> None:
    try:
        scraper.import_materials_from_lesson(lesson)
    except Exception:
        pass


def fetch_timetable(user: "User", start_date: date = None, end_date: date = None, in_thread: bool = True) -> None:
    start_date = start_date or find_next_date_by_weekday(date.today() - timedelta(days=6), weekday=0)
    end_date = end_date or find_next_date_by_weekday(start_date, weekday=4)
    
    scooso_data: "ScoosoData" = user.scoosodata
    
    login_data = {
        "username": scooso_data.username,
        "password": scooso_data.password
    }
    
    with TimetableRequest(**login_data) as scraper:
        data = scraper.get_timetable(start_date, end_date)
        lessons = scraper.import_timetable_from_scraper(data, [user])
        
        for lesson in lessons:
            scraper.import_materials_from_lesson(lesson)
