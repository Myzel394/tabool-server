from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import CreationDateAdminFieldsetMixin, DefaultAdminMixin
from simple_history.admin import SimpleHistoryAdmin

from apps.django.main.school_data.public import model_names as school_names
from ...models import Homework

__all__ = [
    "HomeworkAdmin"
]


@admin.register(Homework)
class HomeworkAdmin(DefaultAdminMixin, SimpleHistoryAdmin):
    fieldset_fields = {
        "default": ["lesson", "due_date", "information", "type", "!..."],
        "extra": ["private_to_user", "!..."]
    }
    list_display = ["__str__", "lesson", "subject", "due_date", "is_private"]
    list_filter = ["lesson__lesson_data__course__subject"]
    search_fields = ["information", "type"]
    autocomplete_fields = ["lesson"]
    date_hierarchy = "created_at"
    mixins = [CreationDateAdminFieldsetMixin]
    
    def is_private(self, instance: Homework) -> bool:
        return instance.is_private
    
    is_private.boolean = True
    is_private.short_description = _("Privat")
    
    def subject(self, instance: Homework):
        return instance.lesson.lesson_data.course.subject
    
    subject.short_description = school_names.SUBJECT
