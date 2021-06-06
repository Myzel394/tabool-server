from datetime import datetime
from typing import *

from django.contrib.auth import login, logout
from django.utils.translation import gettext_lazy as _
from django_hint import RequestType
from rest_framework import status, views
from rest_framework.response import Response

from apps.django.authentication.otp.models import OTP
from apps.django.authentication.otp.utils import is_ip_geolocation_suspicious, send_otp_message
from apps.django.utils.request import get_client_ip
from ....models import KnownIp
from ....serializers import (
    LoginSerializer, UserInformationSerializer,
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

    @staticmethod
    def delete_old_otps():
        # Delete expired
        OTP.objects.only("expire_date").filter(expire_date=datetime.now()).delete()

    def handle_otp(self, user: "User") -> tuple[bool, dict]:
        """
        Checks whether the user has confirmed the OTP. If no OTP available, a new one will be created.
        Deletes old OTPs
        
        :return: Valid, payload
        """
        available_otps = OTP.objects \
            .only("associated_user") \
            .filter(associated_user=user)
        valid_otps = available_otps \
            .only("expire_date") \
            .filter(expire_date__gte=datetime.now())

        user_token = self.request.data.get("otp_key", "")

        # Everything valid, log user in
        if (tokens := valid_otps.only("token").filter(token=user_token)).exists():
            tokens.delete()
            return True, {}

        # OTP expired
        if available_otps.only("token").filter(token=user_token).exists():
            self.create_new_otp(user)
            return False, {
                "otp_key": _("Dieses OTP ist abgelaufen. Es wurde dir ein neues zugeschickt.")
            }

        # No OTP exists, create one
        if valid_otps.count() == 0:
            self.create_new_otp(user)
            return False, {
                "otp_key": _("Kein OTP gefunden (eventuell lange schon abgelaufen?). Es wurde dir ein neues "
                             "zugeschickt.")
            }

        return False, {
            "otp_key": _("Ungültiges OTP.")
        }

    @staticmethod
    def is_ip_known(user: "User", ip_address: str) -> bool:
        return KnownIp.objects.filter(
            associated_user=user,
            ip_address=ip_address,
            expire_date__gte=datetime.now()
        ).exists()

    def post(self, request: RequestType):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # OTP
        ip_address = get_client_ip(request)
        if not self.is_ip_known(user=user, ip_address=ip_address) or is_ip_geolocation_suspicious(ip_address):
            valid, payload = self.handle_otp(user)

            if not valid:
                return Response(payload, status=status.HTTP_401_UNAUTHORIZED)

        self.delete_old_otps()

        # Known ips
        KnownIp.objects.create(
            associated_user=user,
            ip_address=ip_address
        )

        login(request, user)

        user_data = UserInformationSerializer(instance=user).data
        return Response(user_data)


class LogoutView(views.APIView):
    permission_classes = []

    def post(self, request):
        if request.user.is_authenticated:
            # pragma: no cover
            logout(request)

            return Response()
        return Response(status=status.HTTP_202_ACCEPTED)
