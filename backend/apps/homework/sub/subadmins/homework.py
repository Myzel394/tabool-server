from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from apps.lesson.public.admin_inlines import *
from ...models import Homework

__all__ = [
    "HomeworkAdmin"
]


@admin.register(Homework)
class HomeworkAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["due_date", "type"],
        "extra": ["is_private", "information"]
    }
    list_display = ["lesson", "type", "is_private", "due_date"]
    list_filter = ["type", "is_private"]
    search_fields = ["information", "type"]
    inlines = [
        LessonAdminInline
    ]
