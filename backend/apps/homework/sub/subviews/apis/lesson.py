from rest_framework import viewsets

from apps.subject.models import Lesson


class LessonHomeworkViewSet(viewsets.ModelViewSet):
    """Returns homeworks based on lessons"""
    
    queryset = Lesson.objects.all()
    
    def get_queryset(self):
