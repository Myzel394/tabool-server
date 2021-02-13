from rest_framework import viewsets

from apps.django.authentication.user.models import Teacher
from apps.django.authentication.user.sub.subserializers.teacher import DetailTeacherSerializer

__all__ = [
    "TeacherViewSet"
]

from apps.django.utils.permissions import AuthenticationAndActivePermission, IsStudent


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AuthenticationAndActivePermission & IsStudent]
    model = Teacher
    serializer_class = DetailTeacherSerializer
    
    def get_queryset(self):
        return Teacher.objects.all()
