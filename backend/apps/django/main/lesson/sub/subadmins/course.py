from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import field_verbose

from apps.django.main.authentication.models import Student
from ...models import Course

__all__ = [
    "CourseAdmin"
]


@admin.register(Course)
class CourseAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["participants", "subject", "teacher", "course_number", "!..."],
        "created": ["id", "!..."]
    }
    list_display = ["__str__", "subject", "teacher", "class_number", "participants_count"]
    list_filter = ["subject", "teacher"]
    filter_horizontal = ["participants"]
    autocomplete_fields = ["subject", "teacher"]
    search_fields = ["name", "subject", "teacher"]
    
    def class_number(self, instance: Course):
        return instance.get_class_number()
    
    class_number.short_description = field_verbose(Student, "class_number")
    
    def participants_count(self, instance: Course):
        return instance.participants.count()
    
    participants_count.short_description = _("Teilnehmeranzahl")
