from apps.school_data.models import Room, Subject, Teacher
from apps.utils.admin import DefaultAdminInlineMixin


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
        "default": ["first_name", "last_name", "short_name", "email"],
    }
