from rest_framework import views
from rest_framework.response import Response

from apps.authentication.sub.subserializers import PasswordChangerSerializer

__all__ = [
    "PasswordChangeView"
]


class PasswordChangeView(views.APIView):
    def post(self, request):
        serializer = PasswordChangerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = validated_data["user"]
        new_password = validated_data["new_password"]
        
        user.set_password(new_password)
        
        return Response()
