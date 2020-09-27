from dateutil.rrule import DAILY, rrule
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.lesson.models import LessonData
from apps.lesson.serializers import LessonListSerializer
from apps.utils.date import find_next_date_by_weekday
from ....models import Timetable
from ....serializers import LessonAccessSerializer, TimetableDetailSerializer, TimetableListSerializer

__all__ = [
    "TimetableViewSet"
]


# TODO: Change permissions_class "IsAuthenticated" to own, which also validates if a user is active

class TimetableViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return Timetable.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return TimetableListSerializer
        return TimetableDetailSerializer
    
    @action(detail=True)
    def lessons(self, request, pk=None):
        # Check
        serializer = LessonAccessSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        timetable: Timetable = self.get_object()
        
        # Generate
        lesson_data: LessonData
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]
        
        weekdays = {
            date.weekday()
            for date in rrule(DAILY, start_date, until=end_date)
        }
        qs = [
            lesson_data.create_lesson(
                date=find_next_date_by_weekday(start_date, lesson_data.weekday)
            )
            for lesson_data in timetable.lessons_data.all()
            if lesson_data.weekday in weekdays
        ]
        
        # Response
        return Response(
            LessonListSerializer(qs, many=True).data
        )
