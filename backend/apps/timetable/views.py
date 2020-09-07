from rest_framework import viewsets

from .models import Lesson
from .serializers import LessonSerializer

__all__ = [
    "LessonViewSet"
]


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    
    def get_queryset(self):
        return Lesson.objects.all()
