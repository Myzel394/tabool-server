from abc import ABC, abstractmethod

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext_lazy as _
from django_hint import RequestType
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.homework.sub.subserializers import HomeworkBySubjectSerializer
from apps.subject.models import Subject
from apps.subject.sub.subquerysets import SubjectQuerySet
from apps.utils.serializers import ReferencedObjectViewSetMixin

__all__ = [
    "HomeworkBySubjectMixin"
]


class HomeworkBySubjectMixin(
    ReferencedObjectViewSetMixin,
    ABC
):
    permission_classes = [
        IsAuthenticated
    ]
    validated_data_key = "subject"
    validate_serializer_class = HomeworkBySubjectSerializer
    
    @abstractmethod
    def get_queryset(self):
        raise NotImplementedError()
    
    @abstractmethod
    def get_serializer_class(self):
        raise NotImplementedError()
    
    def get_referenced_queryset(self):
        return Subject.objects.all().from_user(self.request.user)
    
    @action(detail=False, url_path="by-subject")
    def by_subject(self, request: RequestType):
        subject = self.parse_to_get_referenced_object(request)
        queryset = self.get_queryset().filter(
            lesson__lesson_data__subject=subject
        )
        
        return self.list_response_from_qs(queryset)
    
    
