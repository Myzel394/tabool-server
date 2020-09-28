from django.contrib.auth.models import Permission

__all__ = [
    "perm_to_permission"
]


def perm_to_permission(identifier: str) -> Permission:
    app_label, codename = identifier.split(".")
    
    return Permission.objects.get(
        content_type__app_label=app_label,
        codename=codename
    )
    
    

