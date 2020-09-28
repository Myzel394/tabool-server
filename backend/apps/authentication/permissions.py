from django_hint import RequestType
from rest_framework import permissions, exceptions

from . import constants

__all__ = [
    "UserPaymentAccessPermission"
]


class UserPaymentAccessPermission(permissions.IsAuthenticated):
    """
    Checks if the user can manage paid users.
    Owners are always allowed, to see their own status.
    """
    perms_map = {
        "GET": [],
        "PUT": [f"{constants.APP_LABEL}.change_userpayment"],
        "PATCH": [f"{constants.APP_LABEL}.change_userpayment"],
    }
    
    def has_permission(self, request: RequestType, view) -> bool:
        if not super().has_permission(request, view):
            return False
    
        if request.method not in self.perms_map:
            raise exceptions.MethodNotAllowed(request.method)
       
        if request.method in permissions.SAFE_METHODS:
            # Check in object
            if view.action == "list":
                return request.user.has_perm(f"{constants.APP_LABEL}.view_userpayment")
            return True
        
        # Deny everything else
        return False
    
    def has_object_permission(self, request: RequestType, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            # Can see if is admin or is owner of the obj
            
            if request.method == "GET":
                return \
                    request.user.has_perm(f"{constants.APP_LABEL}.view_userpayment") \
                    or obj in request.user.payments
        else:
            # Must be admin to edit payments
            return request.user.has_perms(
                self.perms_map[request.method]
            )
    

