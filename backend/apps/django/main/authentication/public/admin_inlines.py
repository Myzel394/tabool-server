from apps.django.utils.admins import DefaultAdminInlineMixin


class UserAdminInline(DefaultAdminInlineMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "id", "!..."]
    }
