from datetime import date, timedelta
from typing import *

from django.conf import settings

from apps.django.main.event.models import Event, Modification
from apps.django.main.event.options import ModificationTypeOptions
from apps.django.main.event.serializers import EventScoosoScraperSerializer, ModificationScoosoScraperSerializer
from apps.django.main.homework.models import Material
from apps.django.main.homework.public import *
from apps.django.main.homework.serializers import MaterialScoosoScraperSerializer
from apps.django.main.lesson.models import Course, Lesson, LessonData, LessonScoosoData
from apps.django.main.lesson.serializers import (
    CourseScoosoScraperSerializer, LessonDataScoosoScraperSerializer, LessonScoosoScraperSerializer,
)
from apps.django.main.school_data.models import Room, Subject, Teacher
from apps.django.main.school_data.serializers import (
    RoomScoosoScraperSerializer, SubjectScoosoScraperSerializer,
    TeacherScoosoScraperSerializer,
)
from .material import MaterialRequest
from .parsers import PureTimetableParser, PureTimetableParserDataType
from .parsers.material import MaterialType
from .parsers.timetable import (
    CourseType, EventType, LessonType, ModificationType, RoomType, SingleEventType, SingleLessonType,
    SingleModificationType, SubjectType, TeacherType,
)
from .request import Request
from .. import constants
from ..utils import build_url, import_from_scraper

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

__all__ = [
    "TimetableRequest"
]


class TimetableRequest(Request):
    def build_get_timetable_url(
            self,
            start_date: date,
            end_date: date
    ) -> str:
        url = constants.TIMETABLE_CONNECTION["url"]
        data = {
            "cmd": 600,
            "subcmd": 100,
            "startDate": start_date.strftime(constants.TIMETABLE_CONNECTION["dt_format"]),
            "endDate": end_date.strftime(constants.TIMETABLE_CONNECTION["dt_format"]),
            **self.login_data
        }
        return build_url(url, data)
    
    def get_timetable(
            self,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None
    ) -> PureTimetableParserDataType:
        start_date = start_date or date.today()
        end_date = end_date or start_date + timedelta(days=5)
        
        return self.request_with_parser(
            parser_class=PureTimetableParser,
            get_data=lambda: {
                "url": self.build_get_timetable_url(
                    start_date=start_date,
                    end_date=end_date
                ),
                "method": constants.TIMETABLE_CONNECTION["method"]
            }
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
            *,
            user: Optional["User"] = None,
            course: Optional[Course] = None,
    ) -> Modification:
        assert user or course, "Either an user or a course must be given."
        
        room = cls.import_room(modification['new_room'], none_on_error=True)
        teacher = cls.import_teacher(modification['new_teacher'])
        subject = cls.import_subject(modification['new_subject'])
        
        if not course:
            course = Course.objects.get(
                course_number=modification['course']['course_number'],
                subject=subject,
                participants__in=[user]
            )
        
        modification = cls.import_modification(
            modification['modification'],
            new_room=room,
            new_teacher=teacher,
            new_subject=subject,
            course=course,
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
                settings.MEDIA_ROOT / build_material_upload_to(material_instance, material['filename'])
            )
            
            material_instance.file = str(path)
            
            materials_list.append(material_instance)
        
        return materials_list
    
    def import_timetable_from_scraper(self, timetable: PureTimetableParserDataType) -> List[Lesson]:
        lessons = []
        # Lessons
        for lesson_data in timetable['lessons']:
            lesson = self.import_lesson_from_scraper(lesson_data)
            lessons.append(lesson)
        
        # Events
        for event in timetable['events']:
            self.import_event_from_scraper(event)
        
        # Modifications
        for modification in timetable['modifications']:
            self.import_modification_from_scraper(modification, course=lessons[0].lesson_data.course)
        
        return lessons