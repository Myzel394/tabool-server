from datetime import date, timedelta
from pathlib import Path
from typing import *

from apps.lesson.models import Course, Lesson, LessonData, LessonScoosoData, Modification, Room, Subject, Teacher
from apps.lesson.serializers import (
    CourseScoosoScraperSerializer, LessonDataScoosoScraperSerializer, LessonScoosoScraperSerializer,
    RoomScoosoScraperSerializer, SubjectScoosoScraperSerializer, TeacherScoosoScraperSerializer,
)
from . import MaterialRequest
from .parsers import PureTimetableParser, PureTimetableParserDataType
from .parsers.material import MaterialType
from .parsers.timetable import (
    CourseType, EventType, LessonType, ModificationType, RoomType, SingleEventType,
    SingleLessonType,
    SingleModificationType, SubjectType, TeacherType,
)
from .request import Request
from .. import constants
from ..utils import build_url, import_from_scraper
from ...event.models import Event
from ...event.options import ModificationTypeOptions
from ...event.sub.subserializers import EventScoosoScraperSerializer
from ...event.sub.subserializers.scooso_scrapers.modification import ModificationScoosoScraperSerializer
from ...homework.models import Material
from ...homework.public import *
from ...homework.sub.subserializers.scooso_scrapers.material import MaterialScoosoScraperSerializer

__all__ = [
    "TimetableRequest"
]


class TimetableRequest(Request):
    def get_timetable(
            self,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None
    ) -> PureTimetableParserDataType:
        start_date = start_date or date.today()
        end_date = end_date or start_date + timedelta(days=5)
        url = constants.TIMETABLE_CONNECTION["url"]
        method = constants.TIMETABLE_CONNECTION["method"]
        
        def get_data():
            data = {
                "cmd": 600,
                "subcmd": 100,
                "startDate": start_date.strftime(constants.TIMETABLE_CONNECTION["dt_format"]),
                "endDate": end_date.strftime(constants.TIMETABLE_CONNECTION["dt_format"]),
                **self.login_data
            }
            return {
                "url": build_url(url, data),
                "method": method
            }
        
        return self.request_with_parser(
            parser_class=PureTimetableParser,
            get_data=get_data
        )
    
    @staticmethod
    def import_teacher(data: TeacherType, **kwargs) -> Teacher:
        return import_from_scraper(TeacherScoosoScraperSerializer, data, **kwargs)
    
    @staticmethod
    def import_room(data: RoomType, **kwargs) -> Room:
        return import_from_scraper(RoomScoosoScraperSerializer, data, **kwargs)
    
    @staticmethod
    def import_subject(data: SubjectType, **kwargs) -> Subject:
        return import_from_scraper(SubjectScoosoScraperSerializer, data, **kwargs)
    
    @staticmethod
    def import_course(data: CourseType, **kwargs) -> Course:
        return import_from_scraper(CourseScoosoScraperSerializer, data, **kwargs)
    
    @staticmethod
    def import_lesson(data: LessonType, **kwargs) -> Lesson:
        return import_from_scraper(LessonScoosoScraperSerializer, data, **kwargs)
    
    @staticmethod
    def import_lesson_data(data: LessonType, **kwargs) -> LessonData:
        return import_from_scraper(LessonDataScoosoScraperSerializer, data, **kwargs)
    
    @staticmethod
    def import_event(data: EventType, **kwargs) -> Event:
        return import_from_scraper(EventScoosoScraperSerializer, data, **kwargs)
    
    @staticmethod
    def import_modification(data: ModificationType, **kwargs) -> Modification:
        return import_from_scraper(ModificationScoosoScraperSerializer, data, **kwargs)
    
    @staticmethod
    def import_material(data: MaterialType, **kwargs) -> Material:
        return import_from_scraper(MaterialScoosoScraperSerializer, data, **kwargs)
    
    @classmethod
    def import_lesson_from_scraper(cls, lesson: SingleLessonType) -> Lesson:
        room = cls.import_room(lesson['room'], none_on_error=True)
        subject = cls.import_subject(lesson['subject'], none_on_error=True)
        teacher = cls.import_teacher(lesson['teacher'], none_on_error=True)
        course = cls.import_course(lesson['course'], none_on_error=True, subject=subject, teacher=teacher)
        lesson_data = cls.import_lesson_data(
            lesson['lesson'],
            room=room,
            course=course,
        )
        lesson = cls.import_lesson(lesson['lesson'], lesson_data=lesson_data)
        
        return lesson
    
    @classmethod
    def import_event_from_scraper(cls, event: SingleEventType) -> Event:
        room = cls.import_room(event['room'], none_on_error=True)
        event = cls.import_event(event['event'], room=room)
        
        return event
    
    @classmethod
    def import_modification_from_scraper(
            cls,
            modification: SingleModificationType,
            modification_type: int = ModificationTypeOptions.REPLACEMENT.value,
    ) -> Modification:
        room = cls.import_room(modification['new_room'], none_on_error=True)
        teacher = cls.import_teacher(modification['new_teacher'])
        subject = cls.import_subject(modification['new_subject'])
        modification = cls.import_modification(
            modification['modification'],
            new_room=room,
            new_teacher=teacher,
            new_subject=subject,
            modification_type=modification_type
        )
        
        return modification
    
    def import_materials_from_lesson(self, lesson: Lesson) -> List[Material]:
        materials_list = []
        scooso_data: LessonScoosoData = lesson.lessonscoosodata
        
        scraper = MaterialRequest(self.username, self.password)
        materials = scraper.get_materials(
            time_id=scooso_data.time_id,
            targeted_date=lesson.date
        )
        
        # Get all materials
        for material in materials['materials']:
            scraper = MaterialRequest(self.username, self.password)
            
            material_instance = self.import_material(
                material,
                lesson=lesson,
            )
            
            path = scraper.download_material(
                material['scooso_id'],
                Path(build_material_upload_to(material_instance, material['filename']))
            )
            
            material_instance.file = str(path)
            
            materials_list.append(material_instance)
        
        return materials_list
