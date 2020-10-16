from typing import *

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django_hint import RequestType
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

if TYPE_CHECKING:
    from ....models import User

__all__ = [
    "email_confirmation"
]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def email_confirmation(request: RequestType):
    user: "User" = request.user
    
    if (key := "confirmation_key") in request.data:
        confirmation_key = request.data[key]
        
        try:
            user.confirm_email(confirmation_key)
        except ObjectDoesNotExist:
            return Response({
                "detail": _("Der Email-Bestätigungscode ist falsch.")
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response()
    return Response({
        "detail": _("Der Email-Bestätigungscode fehlt.")
    }, status=status.HTTP_400_BAD_REQUEST)
