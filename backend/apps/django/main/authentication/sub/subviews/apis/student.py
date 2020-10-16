from rest_framework import generics

from apps.django.main.authentication.models.student import Student
from apps.django.main.authentication.sub.subserializers import StudentSerializer

__all__ = [
    "StudentView"
]


class StudentView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        return Student.objects.all()
    
    def get_object(self):
        return self.get_queryset().get(user=self.request.user)
