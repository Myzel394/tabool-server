from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import field_verbose

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from apps.django.main.school_data.public import model_names as school_names
from ...models import Lesson, LessonData, LessonScoosoData
from ...public import model_names

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
    list_display = ["course_name", "date", "start_time", "end_time", "teacher", "room", ]
    search_fields = ["date", "lesson_data"]
    inlines = [LessonScoosoDataAdminInline]
    
    def course_name(self, instance: Lesson):
        return instance.lesson_data.course.name
    
    course_name.short_description = model_names.COURSE
    
    def teacher(self, instance: Lesson):
        return instance.lesson_data.course.teacher
    
    teacher.short_description = school_names.TEACHER
    
    def room(self, instance: Lesson):
        return instance.lesson_data.room
    
    room.short_description = school_names.ROOM
    
    def start_time(self, instance: Lesson):
        return instance.lesson_data.start_time
    
    start_time.short_description = field_verbose(LessonData, "start_time")
    
    def end_time(self, instance: Lesson):
        return instance.lesson_data.end_time
    
    end_time.short_description = field_verbose(LessonData, "end_time")
