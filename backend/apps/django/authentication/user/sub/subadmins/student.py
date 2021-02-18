from django.contrib import admin
from django.contrib.auth import get_user_model
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import field_verbose

from ...models import Student

__all__ = [
    "StudentAdmin"
]

User = get_user_model()


@admin.register(Student)
class StudentAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["class_number", "main_teacher", "user"],
        "created": ["id"]
    }
    list_display = ["first_name", "last_name", "class_number", "main_teacher__str"]
    search_fields = ["user__first_name", "user__last_name", ]
    
    def first_name(self, student: Student):
        return student.user.first_name
    
    first_name.short_description = field_verbose(User, "first_name")
    
    def last_name(self, student: Student):
        return student.user.first_name
    
    last_name.short_description = field_verbose(User, "last_name")
    
    def main_teacher__str(self, student: Student):
        if student.main_teacher:
            return student.main_teacher.short_name
        return None
    
    def get_readonly_fields(self, request=None, obj=None) -> list:
        base = ["id"]
        
        if obj:
            base += ["user"]
        
        return base
