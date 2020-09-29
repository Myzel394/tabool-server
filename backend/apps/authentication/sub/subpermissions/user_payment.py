from rest_framework import  permissions


__all__ = [
    "IsOwnerPermission"
]


class IsOwnerPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and obj.is_user_owner(request.user)
