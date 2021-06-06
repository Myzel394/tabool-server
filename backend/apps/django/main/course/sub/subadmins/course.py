from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import field_verbose

from apps.django.authentication.user.models import Student
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
    list_filter = ["subject"]
    filter_horizontal = ["participants"]
    autocomplete_fields = ["subject"]
    search_fields = ["subject__name"]

    @staticmethod
    def class_number(instance: Course):
        try:
            return instance.get_class_number()
        except TypeError:
            pass

    class_number.short_description = field_verbose(Student, "class_number")

    @staticmethod
    def participants_count(instance: Course):
        return instance.participants.count()

    participants_count.short_description = _("Teilnehmeranzahl")
