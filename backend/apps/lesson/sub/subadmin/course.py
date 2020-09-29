from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from apps.authentication.public.admin_inlines import UserAdminInline
from ...models import Course
from ...public.admin_inlines import SubjectAdminInline


@admin.register(Course)
class CourseAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["name", "!..."]
    }
    inlines = [
        UserAdminInline, SubjectAdminInline, TeacherAdminInline
    ]
