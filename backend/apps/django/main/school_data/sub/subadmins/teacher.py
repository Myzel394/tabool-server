from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import *

from ...models import Teacher

__all__ = [
    "TeacherAdmin"
]


@admin.register(Teacher)
class TeacherAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "short_name", "email", "!..."],
    }
    
    # TODO: Add teaches_subjects!
