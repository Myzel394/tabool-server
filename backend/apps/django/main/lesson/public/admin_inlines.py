from datetime import time

from apps.django.utils.admins import DefaultAdminInlineMixin
from ..models import Course, Lesson

__all__ = [
    "CourseAdminInline", "LessonAdminInline"
]


class CourseAdminInline(DefaultAdminInlineMixin):
    model = Course
    fieldset_fields = {
        "default": ["name", "get_subject_str", "get_teacher_str", "get_participants_count", "!..."]
    }
    readonly_fields = [
        "get_subject_str", "get_teacher_str", "get_participants_count"
    ]
    
    def get_subject_str(self, obj: Course) -> str:
        return str(obj.subject)
    
    def get_teacher_str(self, obj: Course) -> str:
        return str(obj.teacher)
    
    def get_participants_count(self, obj: Course) -> int:
        return obj.participants.all().count()


class LessonAdminInline(DefaultAdminInlineMixin):
    model = Lesson
    fieldset_fields = {
        "default": ["date", "get_room", "get_course", "get_start_time", "get_end_time", "!..."],
    }
    readonly_fields = [
        "get_lesson_room", "get_lesson_course", "get_lesson_start_time", "get_lesson_end_time"
    ]
    
    def get_lesson_room(self, obj: Lesson) -> str:
        return str(obj.lesson_data.room)
    
    def get_lesson_course(self, obj: Lesson) -> str:
        return str(obj.lesson_data.course)
    
    def get_lesson_start_time(self, obj: Lesson) -> time:
        return obj.lesson_data.start_time
    
    def get_lesson_end_time(self, obj: Lesson) -> time:
        return obj.lesson_data.end_time
