from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...public.model_names import USER

__all__ = [
    "SessionAdmin"
]


@admin.register(Session)
class SessionAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["user_data", "expire_date", "!..."]
    }
    readonly_fields = ["user_data"]
    list_display = ["user_data", "expire_date"]
    date_hierarchy = "expire_date"
    
    def user_data(self, instance: Session):
        UserModel = get_user_model()
        
        session_data = instance.get_decoded()
        user_id = session_data.get("_auth_user_id")
        user = UserModel.objects.only("id").get(id=user_id)
        
        return str(user)
    
    user_data.short_description = USER
