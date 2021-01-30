from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import model_verbose

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from apps.django.main.school_data.models import Teacher
from ...models import Lesson, LessonScoosoData

__all__ = [
    "LessonAdmin"
]


class LessonScoosoDataAdminInline(ScoosoDataAdminInlineMixin):
    model = LessonScoosoData
    fieldset_fields = {
        "default": ["time_id", "lesson_type"]
    }
    readonly_fields = ["time_id", "lesson_type"]


@admin.register(Lesson)
class LessonAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["date", "course", "teacher", "room", "start_time", "end_time", "weekday", ]
    }
    list_display = ["course_name", "date", "start_time", "end_time", "course_teacher", "room", ]
    search_fields = ["course__subject__name", "course__teacher__first_name", "course__teacher__last_name"]
    inlines = [LessonScoosoDataAdminInline]
    
    def course_name(self, instance: Lesson):
        return instance.course.name
    
    course_name.short_description = model_verbose(Lesson)
    
    def course_teacher(self, instance: Lesson):
        return instance.course.teacher
    
    course_teacher.short_description = model_verbose(Teacher)
