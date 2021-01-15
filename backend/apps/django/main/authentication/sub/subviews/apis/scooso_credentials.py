from typing import *

from django.utils.translation import gettext_lazy as _
from django_hint import RequestType
from rest_framework import status, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.django.extra.scooso_scraper.scrapers.request import LoginFailed, Request
from ....serializers import ScoosoChangeSerializer

if TYPE_CHECKING:
    from ....models import ScoosoData


class ScoosoCredentialsView(views.APIView):
    @staticmethod
    def get_put_data(request: RequestType) -> tuple[str, str]:
        """Validates user sent data"""
        
        serializer = ScoosoChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        username = validated_data["username"]
        password = validated_data["password"]
        
        return username, password
    
    @staticmethod
    def validate_scooso_id(request: RequestType, username: str, password: str) -> None:
        """Validate user can login"""
        
        scraper = Request(username, password)
        
        try:
            logged_in_data = scraper.login()
        except LoginFailed:
            raise ValidationError(
                _("Mit diesen Scooso-Anmeldedaten konnte der Server sich nicht anmelden."),
                status.HTTP_400_BAD_REQUEST
            )
        
        # Validate Scooso's user id belongs to request's saved user id
        scooso_data: "ScoosoData" = request.user.scoosodata
        
        if scooso_data.scooso_id != logged_in_data["id"]:
            raise ValidationError(
                _("Dieser Benutzer gehört dir nicht."),
                status.HTTP_400_BAD_REQUEST
            )
    
    @staticmethod
    def is_new_data_equal(request: RequestType, username: str, password: str) -> bool:
        scooso_data = request.user.scoosodata
        
        return scooso_data.username == username and scooso_data.password == password
    
    def get(self, request: RequestType):
        return Response({
            "username": request.user.scoosodata.username,
        })
    
    def put(self, request: RequestType):
        username, password = self.get_put_data(request)
        self.validate_scooso_id(request, username, password)
        
        if self.is_new_data_equal(request, username, password):
            return Response(status=status.HTTP_202_ACCEPTED)
        
        scooso_data = request.user.scoosodata
        
        scooso_data.username = username
        scooso_data.password = password
        scooso_data.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
