from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from apps.django.main.authentication import UserAdminInline
from apps.django.main.school_data.public import SubjectAdminInline
from ...models import Course


@admin.register(Course)
class CourseAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["name", "!..."]
    }
    inlines = [
        UserAdminInline, SubjectAdminInline, TeacherAdminInline
    ]
