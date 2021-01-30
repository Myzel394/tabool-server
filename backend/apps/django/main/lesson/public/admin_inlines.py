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
        "default": ["date", "room", "course", "start_time", "end_time", "!..."],
    }
