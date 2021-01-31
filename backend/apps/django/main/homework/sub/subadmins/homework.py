from typing import *

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import CreationDateAdminFieldsetMixin, DefaultAdminMixin
from django_hint import RequestType
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
    list_filter = ["lesson__course__subject"]
    search_fields = ["information", "type"]
    autocomplete_fields = ["lesson"]
    date_hierarchy = "created_at"
    mixins = [CreationDateAdminFieldsetMixin]
    
    def is_private(self, instance: Homework) -> bool:
        return instance.is_private
    
    is_private.boolean = True
    is_private.short_description = _("Privat")
    
    def subject(self, instance: Homework):
        return instance.lesson.course.subject
    
    subject.short_description = school_names.SUBJECT
    
    def get_queryset(self, request: RequestType):
        if request.user.has_perm("homework.view_private_homework"):
            return Homework.objects.all()
        return Homework.objects.public()
    
    def has_view_permission(self, request: RequestType, obj: Optional[Homework] = None) -> bool:
        if not request.user.has_perm("homework.view_homework"):
            return False
        
        if obj and request:
            return not obj.is_private or \
                   (obj.is_private and request.user.has_perm("homework.can_view_private_homework"))
        return True
