from datetime import date, datetime, time, timedelta
from typing import *

from apps.django.main.event.options import ModificationTypeOptions
from .base import BaseParser

__all__ = [
    "PureTimetableParser", "PureTimetableParserDataType"
]

LESSON_TYPES = {
    "lesson": {100},
    "event": {1},
    "modification": {1010, 1030, 1040, 1050, 1060}
}

LESSON_TYPES_MODIFICATION_TYPE_MAP = {
    1010: ModificationTypeOptions.REPLACEMENT,
    1020: ModificationTypeOptions.ROOM_CHANGE,
    1030: ModificationTypeOptions.REPLACEMENT,
    1040: ModificationTypeOptions.REPLACEMENT,
    1050: ModificationTypeOptions.FREE_PERIOD,
    1060: ModificationTypeOptions.SELF_LEARN,
}

TEACHER_HOMEWORK_KEY = 310


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
    start_datetime: datetime
    end_datetime: datetime


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


class MaterialListDataType(TypedDict):
    time_id: int
    target_date: date


class HomeworkListDataType(TypedDict):
    due_date: datetime


class SingleEventType(TypedDict):
    event: EventType
    room: RoomType


class SingleFreePeriodType(TypedDict):
    period: PeriodType
    room: RoomType
    course: CourseType


class SingleMaterialDataType(TypedDict):
    material: MaterialListDataType
    subject: SubjectType


class SingleHomeworkDataType(TypedDict):
    homework: HomeworkListDataType
    time_id: int


class SingleModificationType(TypedDict):
    new_subject: SubjectType
    new_teacher: TeacherType
    new_room: RoomType
    
    modification: ModificationType
    course: CourseType
    
    time_id: int


class PureTimetableParserDataType(TypedDict):
    lessons: List[SingleLessonType]
    events: List[SingleEventType]
    modifications: List[SingleModificationType]
    materials_data: List[SingleMaterialDataType]
    homeworks: List[SingleHomeworkDataType]


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
        location_code = str(data.get("location_code"))
        
        if (length := len(location_code)) < (max_length := 3) and location_code.isdigit():
            location_code = ("0" * (max_length - length)) + location_code
        
        return {
            "code": location_code,
            "scooso_id": data.get("location")
        }
    
    @classmethod
    def extract_course(cls, data: dict) -> Dict[str, Any]:
        return {
            "course_number": data["coursenumber"],
            "name": data["subject_code"]
        }
    
    @classmethod
    def get_lesson_data(cls, lesson: dict) -> Dict[str, Dict[str, Any]]:
        start_datetime: datetime = lesson["start_time"]
        end_datetime: datetime = lesson["end_time"]
        
        return {
            "lesson": {
                "start_time": start_datetime.time(),
                "end_time": end_datetime.time(),
                "date": start_datetime.date(),
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
        diff: timedelta = event["end_time"] - event["start_time"]
        one_day_diff = datetime.combine(event["end_time"].date(), time.min) \
                       - datetime.combine(event["start_time"].date(), time.min)
        
        is_all_day = event.get("allday", 1) == 1 or diff.microseconds == one_day_diff.microseconds
        
        if is_all_day:
            start_datetime = datetime.combine(event["start_time"].date(), time.min)
            end_datetime = datetime.combine(event["start_time"].date(), time.max)
        else:
            start_datetime = event["start_time"]
            end_datetime = event["end_time"]
        
        return {
            "event": {
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
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
        new_room_code = modification.get("location_code")
        new_room_id = modification.get("location")
        new_teacher_code = modification.get("old_teacher_code")
        new_teacher_id = modification.get("old_teacher")
        
        start_time = modification["start_time"]
        end_time = modification["end_time"]
        
        return {
            "modification": {
                "information": information,
                "start_datetime": start_time,
                "end_datetime": end_time,
                "modification_type": LESSON_TYPES_MODIFICATION_TYPE_MAP[modification["type"]]
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
            "course": cls.extract_course(modification),
            "time_id": modification["time_id"],
        }
    
    @classmethod
    def get_material_data(cls, data: dict) -> Optional[dict]:
        if "materials" in data and \
                (str(TEACHER_HOMEWORK_KEY) in data["materials"]
                 or TEACHER_HOMEWORK_KEY in data["materials"]):
            return {
                "material": {
                    "time_id": data["time_id"],
                    "target_date": data["start_time"].date(),
                },
                "subject": cls.extract_subject(data),
            }
        return
    
    @classmethod
    def get_homework_data(cls, data: dict) -> Optional[dict]:
        if value := data.get("homework_until"):
            print(value)
            return {
                "homework": {
                    "due_date": value,
                },
                "time_id": data["time_id"]
            }
        return
    
    @property
    def is_valid(self) -> bool:
        try:
            return self.json["item"].get("code", None) is not None
        except:
            return False
    
    @staticmethod
    def is_lesson(thing: dict) -> bool:
        return thing.get("lessontype", None) == 100 or "lessontype" in thing and "new_subject" not in thing
    
    @staticmethod
    def is_event(thing: dict) -> bool:
        return "lessontype" not in thing and "event_id" in thing and "new_subject" not in thing
    
    @staticmethod
    def is_modification(thing: dict) -> bool:
        return "new_subject" in thing
    
    @property
    def data(self) -> PureTimetableParserDataType:
        lessons = []
        events = []
        modifications = []
        materials = []
        homeworks = []
        
        for thing in self.json["tables"]["schedule"]:
            if self.is_lesson(thing):
                lessons.append(self.get_lesson_data(thing))
            elif self.is_event(thing):
                events.append(self.get_event_data(thing))
            elif self.is_modification(thing):
                modifications.append(self.get_modification_data(thing))
            
            if data := self.get_material_data(thing):
                materials.append(data)
            
            if data := self.get_homework_data(thing):
                homeworks.append(data)
        
        return {
            "lessons": lessons,
            "events": events,
            "modifications": modifications,
            "materials_data": materials,
            "homeworks": homeworks
        }
