from django.contrib.auth import login, logout
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ....serializers import (
    LoginSerializer, UserInformationSerializer,
)

__all__ = [
    "LoginView", "LogoutView"
]


class LoginView(views.APIView):
    permission_classes = [
        ~IsAuthenticated
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
