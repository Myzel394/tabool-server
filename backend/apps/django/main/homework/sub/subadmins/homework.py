from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Homework


@admin.register(Homework)
class HomeworkAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["type", "due_date", "information"],
        "advanced": ["private_to_student", "lesson", "lesson_date"]
    }
    list_display = ["__str__", "due_date", "is_private", "type"]
    list_filter = ["type"]
    date_hierarchy = "due_date"
    autocomplete_fields = ["lesson"]
    search_fields = ["lesson__course__subject__name", ]
    
    def is_private(self, instance: Homework) -> bool:
        return instance.is_private
    
    is_private.boolean = True
