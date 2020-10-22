from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.metadata import SimpleMetadata
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ....serializers import (
    FullRegistrationSerializer, RegisterSerializer, ScoosoDataRegistrationSerializer, StudentRegistrationSerializer,
    UserInformationSerializer,
)

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
        
        login(request, user)
        
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
