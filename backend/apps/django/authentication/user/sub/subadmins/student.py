from django.contrib import admin
from django.contrib.auth import get_user_model
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import field_verbose

from ...models import Student

__all__ = [
    "StudentAdmin"
]

User = get_user_model()


@admin.register(Student)
class StudentAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["class_number", "main_teacher", "user"],
        "created": ["id"]
    }
    list_display = ["first_name", "last_name", "class_number", "main_teacher__str"]
    search_fields = ["user__first_name", "user__last_name", ]

    @staticmethod
    def first_name(student: Student):
        return student.user.first_name

    first_name.short_description = field_verbose(User, "first_name")

    @staticmethod
    def last_name(student: Student):
        return student.user.first_name

    last_name.short_description = field_verbose(User, "last_name")

    @staticmethod
    def main_teacher__str(student: Student):
        if student.main_teacher:
            return student.main_teacher.short_name
        return None

    @staticmethod
    def get_readonly_fields(request=None, obj=None) -> list:
        base = ["id"]

        if obj:
            base += ["user"]

        return base
