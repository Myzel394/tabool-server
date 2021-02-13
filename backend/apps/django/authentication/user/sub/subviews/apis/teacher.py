from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.django.authentication.user.models import Teacher
from apps.django.authentication.user.sub.subserializers.teacher import DetailTeacherSerializer
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsStudent

__all__ = [
    "TeacherViewSet"
]


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AuthenticationAndActivePermission & IsStudent]
    
    filter_backends = [SearchFilter]
    search_fields = ["user__first_name", "user__last_name"]
    
    model = Teacher
    serializer_class = DetailTeacherSerializer
    
    def get_queryset(self):
        return Teacher.objects.all()
