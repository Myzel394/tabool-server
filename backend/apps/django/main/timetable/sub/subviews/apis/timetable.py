from django_hint import RequestType
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.django.utils.permissions import AuthenticationAndActivePermission, IsStudent, IsTeacher
from ....models import Lesson, Timetable
from ....serializers import StudentDetailTimetableSerializer, TeacherDetailLessonSerializer

__all__ = [
    "StudentTimetableViewSet", "TeacherTimetableViewSet"
]


class StudentTimetableViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.RetrieveModelMixin
):
    permission_classes = [AuthenticationAndActivePermission & IsStudent]
    serializer_class = StudentDetailTimetableSerializer
    
    def get_queryset(self):
        return Timetable.objects.from_user(self.request.user)
    
    @action(["GET"], detail=False)
    def current(self, request: RequestType):
        current_timetable = Timetable.objects.current(self.request.user)
        serializer = self.serializer_class(current_timetable, context={
            "request": self.request
        })
        
        return Response(serializer.data)


class TeacherTimetableViewSet(
    viewsets.GenericViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacher]
    # No implementation needed
    queryset = None
    
    @action(["GET"], detail=False)
    def current(self, request: RequestType):
        lessons = Lesson.objects.from_user(self.request.user)
        
        serializer = TeacherDetailLessonSerializer(lessons, many=True, context={
            "request": self.request
        })
        
        # Return dict in case more fields will be added
        return Response({
            "lessons": serializer.data
        })
