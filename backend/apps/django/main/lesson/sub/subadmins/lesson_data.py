import calendar

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from apps.django.main.school_data.public import model_names as school_names
from apps.utils import format_datetime
from ...models import LessonData, LessonDataScoosoData
from ...public import model_names

__all__ = [
    "LessonDataAdmin"
]


class LessonDataScoosoDataAdminInline(ScoosoDataAdminInlineMixin):
    model = LessonDataScoosoData
    fieldset_fields = {
        "default": ["lesson_type"]
    }


@admin.register(LessonData)
class LessonDataAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["course", "room", "start_time", "end_time", "weekday", "!..."]
    }
    list_display = ["course_name", "teacher", "room", "date"]
    list_filter = ["course", "course__subject", "course__teacher", "room", "weekday"]
    autocomplete_fields = ["course", "room"]
    inlines = [LessonDataScoosoDataAdminInline]
    
    def course_name(self, instance: LessonData):
        return instance.course.name
    
    course_name.short_description = model_names.COURSE
    
    def teacher(self, instance: LessonData):
        return instance.course.teacher
    
    teacher.short_description = school_names.TEACHER
    
    def date(self, instance: LessonData):
        abbreviations = list(calendar.day_abbr)
        date_abbr = abbreviations[instance.weekday]
        
        return f"{date_abbr} {format_datetime(instance.start_time)} - {format_datetime(instance.end_time)}"
    
    date.short_description = _("Datum")
