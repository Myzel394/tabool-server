from django.contrib.auth import login, logout
from django_hint import RequestType
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ....serializers import (
    LoginSerializer, UserInformationSerializer,
)

__all__ = [
    "LoginView", "LogoutView", "IsAuthenticatedView"
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


class IsAuthenticatedView(APIView):
    def get(self, request: RequestType):
        return Response({
            "is_authenticated": request.user.is_authenticated
        })
