from typing import *

from django_hint import RequestType
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

if TYPE_CHECKING:
    from ....models import User

__all__ = [
    "email_confirmation"
]


@api_view(["POST"])
@authentication_classes([IsAuthenticated])
def email_confirmation(request: RequestType):
    user: "User" = request.user
    
    if (key := "confirmation_key") in request.POST:
        confirmation_key = request.POST[key]
        
        user.confirm_email(confirmation_key)
        
        if user.is_confirmed:
            return Response()
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
