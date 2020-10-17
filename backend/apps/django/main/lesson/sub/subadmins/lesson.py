from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from ...models import Lesson, LessonScoosoData

__all__ = [
    "LessonAdmin"
]


class LessonScoosoDataAdminInline(ScoosoDataAdminInlineMixin):
    model = LessonScoosoData
    fieldset_fields = {
        "default": ["time_id"]
    }


@admin.register(Lesson)
class LessonAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["date", "lesson_data"]
    }
    list_display = ["date"]
    search_fields = ["date", "lesson_data"]
    inlines = [LessonScoosoDataAdminInline]
