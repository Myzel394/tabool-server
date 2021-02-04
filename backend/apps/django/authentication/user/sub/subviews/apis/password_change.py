from django.contrib.auth import update_session_auth_hash
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ....serializers import PasswordChangerSerializer

__all__ = [
    "PasswordChangeView"
]


class PasswordChangeView(views.APIView):
    permission_classes = [
        IsAuthenticated
    ]
    
    def post(self, request):
        serializer = PasswordChangerSerializer(data=request.data, context={
            "request": request,
        })
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        validated_data = serializer.validated_data
        
        new_password = validated_data["new_password"]
        
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
