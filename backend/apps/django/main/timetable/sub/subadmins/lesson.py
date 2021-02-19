from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Lesson


@admin.register(Lesson)
class LessonAdmin(DefaultAdminMixin):
    search_fields = ["course__subject__name"]
    autocomplete_fields = ["course"]
