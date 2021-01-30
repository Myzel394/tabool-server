from datetime import date, datetime, time, timedelta

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_hint import RequestType
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.django.main.event.models import Event, Exam, Modification
from apps.django.main.event.sub.subserializers.event.detail import DetailEventSerializer
from apps.django.main.event.sub.subserializers.exam.detail import DetailExamSerializer
from apps.django.main.event.sub.subserializers.modification.detail import DetailModificationSerializer
from apps.django.main.homework.models import Homework, Material
from apps.django.main.homework.sub.subserializers.homework.detail import DetailHomeworkSerializer
from apps.django.main.homework.sub.subserializers.material.detail import DetailMaterialSerializer
from ....models import Lesson
from ....serializers import DailyDataSerializer, RelatedDetailLessonSerializer


@api_view(["GET"])
def daily_data(request: RequestType):
    # Validation
    serializer = DailyDataSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    
    # Variables
    user = request.user
    serializer_context = {
        "request": request
    }
    data = serializer.validated_data
    targeted_date: date = data["date"]
    targeted_date_range = (
        datetime.combine(targeted_date, time.min),
        datetime.combine(targeted_date, time.max)
    )
    max_future_days: int = data["max_future_days"]
    
    # Empty guard
    if Lesson.objects.count() == 0:
        return Response({
            "detail": _("Der Stundenplan wurde noch nicht geladen.")
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Get data
    user_lessons = Lesson.objects \
        .from_user(user)
    lessons = user_lessons \
        .only("date") \
        .filter(date=targeted_date) \
        .order_by("start_time")
    course_ids = lessons.values_list("course", flat=True).distinct()
    modifications = Modification.objects \
        .only("lesson") \
        .filter(lesson__in=lessons) \
        .distinct()
    homeworks = Homework.objects \
        .only("lesson", "due_date") \
        .filter(Q(userhomeworkrelation__isnull=True) | Q(userhomeworkrelation__completed=False)) \
        .filter(Q(lesson__in=lessons) | Q(due_date__range=targeted_date_range)) \
        .distinct()
    exams = Exam.objects \
        .only("course", "targeted_date") \
        .filter(course__id__in=course_ids,
                targeted_date__gte=targeted_date,
                targeted_date__lte=targeted_date + timedelta(days=max_future_days)) \
        .distinct()
    events = Event.objects \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=datetime.combine(targeted_date, time.min),
                end_datetime__lte=datetime.combine(targeted_date + timedelta(days=max_future_days), time.max)) \
        .distinct()
    video_conference_lessons = Lesson.objects \
        .from_user(user) \
        .only("video_conference_link", "date") \
        .filter(video_conference_link__isnull=False,
                date__gte=targeted_date,
                date__lte=targeted_date + timedelta(days=max_future_days)) \
        .distinct()
    materials = Material.objects \
        .only("lesson") \
        .filter(lesson__in=lessons)
    
    return Response({
        "lessons": RelatedDetailLessonSerializer(lessons, many=True, context=serializer_context).data,
        "modifications": DetailModificationSerializer(
            modifications, many=True, context=serializer_context
        ).data,
        "homeworks": DetailHomeworkSerializer(homeworks, many=True, context=serializer_context).data,
        "exams": DetailExamSerializer(exams, many=True, context=serializer_context).data,
        "events": DetailEventSerializer(events, many=True, context=serializer_context).data,
        "materials": DetailMaterialSerializer(materials, many=True, context=serializer_context).data,
        "video_conference_lessons": RelatedDetailLessonSerializer(
            video_conference_lessons, many=True, context=serializer_context
        ).data,
        "earliest_date_available": user_lessons.only("date").earliest("date").date,
        "latest_date_available": user_lessons.only("date").latest("date").date
    })
