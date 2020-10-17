from apps.django.main.school_data.models import Room, Subject, Teacher
from apps.django.utils.admins import DefaultAdminInlineMixin

__all__ = [
    "SubjectAdminInline", "RoomAdminInline", "TeacherAdminInline"
]


class SubjectAdminInline(DefaultAdminInlineMixin):
    model = Subject
    fieldset_fields = {
        "default": ["name", "color", "!..."]
    }


class RoomAdminInline(DefaultAdminInlineMixin):
    model = Room
    fieldset_fields = {
        "default": ["place", "!..."]
    }


class TeacherAdminInline(DefaultAdminInlineMixin):
    model = Teacher
    fieldset_fields = {
        "default": ["first_name", "last_name", "short_name", "email", "!..."],
    }
