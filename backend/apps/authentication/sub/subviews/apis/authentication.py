from django.contrib.auth import login, logout
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated, NOT
from rest_framework.response import Response

from ....serializers import LoginSerializer, RegisterSerializer, UserInformationSerializer

__all__ = [
    "LoginView", "LogoutView", "RegisterView"
]


class LoginView(views.APIView):
    permission_classes = [
        NOT(IsAuthenticated)
    ]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = validated_data["user"]
        
        login(request, user)
        user_data = UserInformationSerializer(user).data
        
        return Response(user_data)


class LogoutView(views.APIView):
    permission_classes = [
        IsAuthenticated
    ]
    
    def post(self, request):
        logout(request)
        
        return Response()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer: RegisterSerializer):
        user = serializer.save()
        login(self.request, user)
        return user
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.perform_create(serializer)
        serializer = UserInformationSerializer(user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
