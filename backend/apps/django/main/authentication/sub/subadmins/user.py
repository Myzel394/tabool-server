from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Student, User

__all__ = [
    "UserAdmin"
]


class StudentAdminInline(admin.StackedInline):
    model = Student
    fields = ["main_teacher", "class_number"]
    min_num = 0
    max_num = 0
    autocomplete_fields = ["main_teacher"]


@admin.register(User)
class UserAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["email", "id", "is_active", "!..."]
    }
    list_display = ["email", "id", "is_active", "is_confirmed"]
    list_filter = ["is_active"]
    inlines = [StudentAdminInline]
