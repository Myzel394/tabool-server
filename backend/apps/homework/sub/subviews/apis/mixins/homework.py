from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.homework.sub.subserializers import HomeworkBySubjectSerializer
from apps.subject.models import Subject
from apps.subject.sub.subquerysets import SubjectQuerySet


class HomeworkBySubjectMixin(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    # TODO: Diese Klasse verallgemeinern (mit Reference object etc)
    
    def get_subject_queryset(self) -> SubjectQuerySet:
        return Subject.objects.all().from_user(self.request.user)
    
    def get_subject(self, validated_data: dict) -> Subject:
        try:
            return self.get_subject_queryset().only("id").get(id=validated_data["subject"])
        except ObjectDoesNotExist:
            raise ValidationError(_("Das Element konnte nicht gefunden werden."), "reference_not_found")
    
    @action(detail=False, url_path="by-subject")
    def by_subject(self, request: WSGIRequest):
        # Validating
        serializer = HomeworkBySubjectSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        subject = self.get_subject(validated_data)
        
        # Filtering
        queryset = self.get_queryset().filter(lesson__lesson_data__subject=subject)
        
        # Output
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
