from typing import *

from django.contrib.auth import logout
from rest_framework import generics, status
from rest_framework.metadata import SimpleMetadata
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ....serializers import (
    FullRegistrationSerializer, RegisterSerializer, ScoosoDataRegistrationSerializer, StudentRegistrationSerializer,
    UserInformationSerializer,
)

if TYPE_CHECKING:
    from ....models import User

__all__ = [
    "RegisterView", "FullRegisterView"
]


class RegisterView(generics.CreateAPIView):
    permission_classes = [
        ~IsAuthenticated
    ]
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer: RegisterSerializer):
        user = serializer.save()
        return user
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.perform_create(serializer)
        serializer = UserInformationSerializer(user)
        
        logout(request)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FullRegisterView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FullRegistrationSerializer
    
    def options(self, request, *args, **kwargs):
        metadata = SimpleMetadata()
        
        return Response({
            "actions": {
                "POST": {
                    "student": metadata.get_serializer_info(StudentRegistrationSerializer()),
                    "scoosodata": metadata.get_serializer_info(ScoosoDataRegistrationSerializer())
                }
            }
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        user: "User" = serializer.instance
        
        user.scoosodata.fetch_user_data()
        
        return Response(
            UserInformationSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
