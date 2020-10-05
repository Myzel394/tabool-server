from datetime import date, datetime, time
from typing import *

from .base import BaseParser

__all__ = [
    "PureTimetableParser", "PureTimetableParserDataType"
]

LESSON_TYPES = {
    "lesson": [100],
    "event": [1],
    "modification": [1030, 1040, 1050, 1060]
}


class DefaultScoosoDataTypeMixin(TypedDict):
    code: Optional[str]
    scooso_id: Optional[int]


class RoomType(DefaultScoosoDataTypeMixin):
    pass


class SubjectType(DefaultScoosoDataTypeMixin):
    pass


class TeacherType(DefaultScoosoDataTypeMixin):
    pass


class CourseType(TypedDict):
    course_number: Optional[int]
    name: Optional[str]


class LessonType(TypedDict):
    time_id: int
    lesson_type: str
    
    start_time: time
    end_time: time
    weekday: int
    date: date


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


class EventType(TypedDict):
    start_time: time
    end_time: time
    title: str


class MaterialType(TypedDict):
    calendar_id: int
    time_id: int
    target_date: date


class SingleEventType(TypedDict):
    event: EventType
    room: RoomType


class SingleFreePeriodType(TypedDict):
    period: PeriodType
    room: RoomType
    course: CourseType


class SingleMaterialDataType(TypedDict):
    material: MaterialType
    subject: SubjectType


class SingleModificationType(TypedDict):
    modification: ModificationType
    new_subject: SubjectType
    new_teacher: TeacherType
    new_room: RoomType
    
    # TODO: Add time_id, targeted_date etc as meta (or lesson)


class PureTimetableParserDataType(TypedDict):
    lessons: List[SingleLessonType]
    events: List[SingleEventType]
    modifications: List[SingleModificationType]
    materials_data: List[SingleMaterialDataType]


class PureTimetableParser(BaseParser):
    @staticmethod
    def build_course_name(subject: str, course_number: int) -> Optional[str]:
        return f"{subject or ''}{course_number or ''}" or None
    
    @staticmethod
    def extract_subject(data: dict) -> Dict[str, Any]:
        return {
            "code": data.get("subject_code"),
            "scooso_id": data.get("subject")
        }
    
    @staticmethod
    def extract_teacher(data: dict) -> Dict[str, Any]:
        return {
            "code": data.get("teacher_code"),
            "scooso_id": data.get("teacher")
        }
    
    @staticmethod
    def extract_room(data: dict) -> Dict[str, Any]:
        return {
            "code": str(data.get("location_code")),
            "scooso_id": data.get("location")
        }
    
    @classmethod
    def extract_course(cls, data: dict) -> Dict[str, Any]:
        return {
            "course_number": int(data["coursenumber"]),
        }
    
    @classmethod
    def get_lesson_data(cls, lesson: dict) -> Dict[str, Dict[str, Any]]:
        start_datetime: datetime = lesson["start_time"]
        end_datetime: datetime = lesson["end_time"]
        
        return {
            "lesson": {
                "start_time": start_datetime.time(),
                "end_time": end_datetime.time(),
                "date": start_datetime.date(),  # TODO: Remove `weekday` here, it can be extracted from `date`
                "weekday": start_datetime.date().weekday(),
                "time_id": lesson["time_id"],
                "lesson_type": lesson["lessontype"]
            },
            "room": cls.extract_room(lesson),
            "subject": cls.extract_subject(lesson),
            "teacher": cls.extract_teacher(lesson),
            "course": cls.extract_course(lesson),
        }
    
    @classmethod
    def get_event_data(cls, event: dict) -> Dict[str, Any]:
        return {
            "event": {
                "start_datetime": event["start_time"],
                "end_datetime": event["end_time"],
                "is_all_day": event.get("allday", 1) == 1,
                "title": event.get("title") or None
            },
            "room": cls.extract_room(event)
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
    def get_modification_data(cls, modification: dict) -> Dict[str, Any]:
        information = modification.get("information") or None
        
        new_subject_code = modification.get("subject_code")
        new_subject_id = modification.get("subject")
        new_room_code = modification.get("new_location_code")
        new_room_id = modification.get("new_location")
        new_teacher_code = modification.get("old_teacher_code")
        new_teacher_id = modification.get("old_teacher")
        
        start_time = modification["start_time"]
        end_time = modification["end_time"]
        
        return {
            "modification": {
                "information": information,
                "start_datetime": start_time,
                "end_datetime": end_time
            },
            "new_subject": {
                "code": new_subject_code,
                "scooso_id": new_subject_id
            },
            "new_teacher": {
                "code": new_teacher_code,
                "scooso_id": new_teacher_id
            },
            "new_room": {
                "code": new_room_code,
                "scooso_id": new_room_id
            },
            "new_course": {
                "course_number": modification.get("coursenumber")
            },
            "course": cls.extract_course(modification),
        }
    
    @classmethod
    def get_material_data(cls, data: dict) -> Optional[dict]:
        if (key := "materials") in data:
            prop = next(iter(data[key]))
            
            return {
                "material": {
                    "time_id": data["time_id"],
                    "target_date": data["start_time"].date(),
                    "calendar_id": int(prop),
                },
                "subject": cls.extract_subject(data),
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
            elif lesson_type in LESSON_TYPES["modification"]:
                modifications.append(self.get_modification_data(thing))
            
            if data := self.get_material_data(thing):
                materials.append(data)
        
        return {
            "lessons": lessons,
            "events": events,
            "modifications": modifications,
            "materials_data": materials
        }
