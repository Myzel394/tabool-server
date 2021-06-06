from django.contrib import admin
from django.contrib.auth import get_user_model
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import field_verbose

from ...models import Teacher

__all__ = [
    "TeacherAdmin"
]

User = get_user_model()


@admin.register(Teacher)
class TeacherAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["short_name", "user"],
        "created": ["id"]
    }
    list_display = ["short_name", "first_name", "last_name"]
    search_fields = ["user__first_name", "user__last_name", "short_name"]

    @staticmethod
    def first_name(teacher: Teacher):
        return teacher.user.first_name

    first_name.short_description = field_verbose(User, "first_name")

    @staticmethod
    def last_name(teacher: Teacher):
        return teacher.user.first_name

    last_name.short_description = field_verbose(User, "last_name")

    @staticmethod
    def get_readonly_fields(request=None, obj=None) -> list:
        base = ["id"]

        if obj:
            base += ["user"]

        return base
