from datetime import datetime, timedelta
from typing import *

from django.contrib.auth import login, logout
from django.utils.translation import gettext_lazy as _
from django_hint import RequestType
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.django.main.otp.constants import OTP_EXPIRE_DURATION
from apps.django.main.otp.models.otp import OTP
from apps.django.main.otp.utils import is_ip_geolocation_suspicious, send_otp_message
from apps.django.utils.request import get_client_ip
from ....serializers import (
    LoginSerializer, UserAuthenticationSerializer,
)

if TYPE_CHECKING:
    from ....models import User

__all__ = [
    "LoginView", "LogoutView"
]


class LoginView(views.APIView):
    permission_classes = []
    
    def create_new_otp(self, user: "User"):
        otp = OTP.objects.create(
            associated_user=user
        )
        send_otp_message(request=self.request, user=user, otp=otp)
    
    def has_confirmed_otp(self, request: RequestType, user: "User") -> tuple[bool, bool, dict]:
        """
        Checks whether the user has confirmed the OTP. If no OTP available, a new one will be created.
        
        :return: Valid, New OTP created?, payload
        """
        
        available_otps = OTP.objects.only("associated_user").filter(associated_user=user)
        valid_otps = available_otps \
            .only("expire_date") \
            .filter(expire_date__gte=datetime.now() - timedelta(minutes=OTP_EXPIRE_DURATION))
        
        if valid_otps.count() > 0:
            if (token := request.data.get("otp_key", "")) != "":
                for otp in valid_otps:  # type: OTP
                    if otp.is_valid(token):
                        return True, False, {}
                
                # Check if OTP is expired
                if available_otps.only("token").filter(token=token).exists():
                    self.create_new_otp(user)
                    return False, False, {
                        "otp_key": _("Dieses OTP ist abgelaufen. Es wurde dir ein neues zugeschickt.")
                    }
            
            return False, False, {
                "otp_key": _("Ungültiges OTP.")
            }
        else:
            self.create_new_otp(user)
            return False, True, {}
    
    def post(self, request: RequestType):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        
        ip = get_client_ip(request)
        if is_ip_geolocation_suspicious(ip):
            valid, otp_created, payload = self.has_confirmed_otp(request, user)
            
            if not valid:
                if otp_created:
                    return Response(payload, status=status.HTTP_401_UNAUTHORIZED)
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)
        user_data = UserAuthenticationSerializer(user).data
        
        return Response(user_data)


class LogoutView(views.APIView):
    permission_classes = [
        IsAuthenticated
    ]
    
    def post(self, request):
        logout(request)
        
        return Response()
