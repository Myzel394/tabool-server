from datetime import datetime, time
from typing import *

from .base import BaseParser

__all__ = [
    "PureTimetableParser", "PureTimetableParserDataType"
]

LESSON_TYPES = {
    "lesson": [100],
    "event": [1],
    "freePeriod": [1050, 1060],
    "replace": [1030, 1040]
}


class DefaultScoosoDataTypeMixin(TypedDict):
    code: Optional[str]
    id: Optional[int]


class RoomType(DefaultScoosoDataTypeMixin):
    pass


class SubjectType(DefaultScoosoDataTypeMixin):
    pass


class TeacherType(DefaultScoosoDataTypeMixin):
    pass


class CourseType(TypedDict):
    course_number: Optional[int]
    suggested_name: Optional[str]


class LessonType(TypedDict):
    start_time: time
    end_time: time


class ModificationType(TypedDict):
    information: Optional[str]
    start_time: time
    end_time: time


class PeriodType(TypedDict):
    information: Optional[str]


class SingleLessonType(TypedDict):
    lesson: LessonType
    room: RoomType
    subject: SubjectType
    teacher: TeacherType
    course: CourseType


class SingleEventType(TypedDict):
    start_time: time
    end_time: time
    title: str


class SingleFreePeriodType(TypedDict):
    period: PeriodType
    room: RoomType
    course: CourseType


class SingleMaterialsDataType(TypedDict):
    calendar_id: int
    time_id: int
    subject_id: int


class SingleModificationType(TypedDict):
    modification: ModificationType
    subject: SubjectType
    teacher: TeacherType
    room: RoomType


class PureTimetableParserDataType(TypedDict):
    lessons: List[SingleLessonType]
    events: List[SingleEventType]
    modifications: List[SingleModificationType]
    free_periods: List[SingleFreePeriodType]
    materials_data: List[SingleMaterialsDataType]


class PureTimetableParser(BaseParser):
    @staticmethod
    def build_course_name(subject: str, course_number: int) -> Optional[str]:
        return f"{subject or ''}{course_number or ''}" or None
    
    @staticmethod
    def extract_subject(data: dict) -> Dict[str, Any]:
        return {
            "code": data.get("subject_code"),
            "id": data.get("subject")
        }
    
    @staticmethod
    def extract_teacher(data: dict) -> Dict[str, Any]:
        return {
            "code": data.get("teacher_code"),
            "id": data.get("teacher")
        }
    
    @staticmethod
    def extract_room(data: dict) -> Dict[str, Any]:
        return {
            "code": data.get("location_code"),
            "id": data.get("location")
        }
    
    @classmethod
    def extract_course(cls, data: dict) -> Dict[str, Any]:
        course_number = data.get("coursenumber")
        
        return {
            "course_number": int(course_number) if course_number else None,
            "suggested_name": cls.build_course_name(data.get("subject_code"), course_number)
        }
    
    @classmethod
    def get_lesson_data(cls, lesson: dict) -> Dict[str, Dict[str, Any]]:
        start_datetime: datetime = lesson["start_time"]
        end_datetime: datetime = lesson["end_time"]
        
        return {
            "lesson": {
                "start_time": start_datetime.time(),
                "end_time": end_datetime.time(),
            },
            "room": cls.extract_room(lesson),
            "subject": cls.extract_subject(lesson),
            "teacher": cls.extract_teacher(lesson),
            "course": cls.extract_course(lesson),
        }
    
    @staticmethod
    def get_event_data(event: dict) -> Dict[str, Any]:
        default_data = {
            "title": event.get("title") or None,
        }
        
        if event.get("allday", 1) == 1:
            return {
                "is_all_day": True,
                **default_data
            }
        return {
            "start_time": event["start_time"].time(),
            "end_time": event["end_time"].time(),
            **default_data
        }
    
    @classmethod
    def get_freeperiod_data(cls, period: dict) -> Dict[str, Any]:
        return {
            "period": {
                "information": period.get("information") or None
            },
            "room": cls.extract_room(period),
            "course": cls.extract_course(period),
        }
    
    @classmethod
    def get_replacement_data(cls, replace: dict) -> Dict[str, Any]:
        information = replace.get("information") or None
        
        new_subject_code = replace.get("subject_code")
        new_subject_id = replace.get("subject")
        new_room_code = replace.get("new_location_code")
        new_room_id = replace.get("new_location")
        new_teacher_code = replace.get("old_teacher_code")
        new_teacher_id = replace.get("old_teacher")
        
        start_time = replace["start_time"]
        end_time = replace["end_time"]
        
        return {
            "modification": {
                "information": information,
                "start_time": start_time,
                "end_time": end_time
            },
            "subject": {
                "code": new_subject_code,
                "id": new_subject_id
            },
            "teacher": {
                "code": new_teacher_code,
                "id": new_teacher_id
            },
            "room": {
                "code": new_room_code,
                "id": new_room_id
            }
        }
    
    @staticmethod
    def get_material_data(data: dict) -> Optional[dict]:
        if (key := "materials") in data:
            prop = next(iter(data[key]))
            
            return {
                "calendar_id": int(prop),
                "time_id": data["time_id"],
                "subject_id": data["subject"]
            }
        return None
    
    @property
    def is_valid(self) -> bool:
        try:
            return self.json["item"].get("code", None) is not None
        except:
            return False
    
    @property
    def data(self) -> PureTimetableParserDataType:
        lessons = []
        events = []
        modifications = []
        free_periods = []
        materials = []
        
        for thing in self.json["tables"]["schedule"]:
            lesson_type = thing["type"]
            if lesson_type in LESSON_TYPES["lesson"]:
                lessons.append(self.get_lesson_data(thing))
            elif lesson_type in LESSON_TYPES["event"]:
                events.append(self.get_event_data(thing))
            elif lesson_type in LESSON_TYPES["freePeriod"]:
                free_periods.append(self.get_freeperiod_data(thing))
            elif lesson_type in LESSON_TYPES["replace"]:
                modifications.append(self.get_replacement_data(thing))
            
            if data := self.get_material_data(thing):
                materials.append(data)
        
        return {
            "lessons": lessons,
            "events": events,
            "modifications": modifications,
            "free_periods": free_periods,
            "materials_data": materials
        }
