from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.django.utils.viewsets import BulkDeleteMixin
from ....filters import HomeworkFilterSet
from ....models import Homework
from ....serializers import HomeworkDetailEndpointSerializer, HomeworkListSerializer

__all__ = [
    "HomeworkViewSet"
]


class HomeworkViewSet(viewsets.ModelViewSet, BulkDeleteMixin):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HomeworkFilterSet
    search_fields = ["information"]
    ordering_fields = ["due_date"]  # TODO: Add user relation ordering!
    
    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return Homework.objects.from_user(self.request.user).distinct()
        return Homework.objects.only("private_to_user").filter(private_to_user=self.request.user).distinct()
    
    def get_serializer_class(self):
        if self.action == "list":
            return HomeworkListSerializer
        return HomeworkDetailEndpointSerializer
    
    @action(methods=["GET"], detail=False, url_path="homework-information")
    def information(self, request: RequestType):
        homeworks = Homework.objects.from_user(request.user)
        
        earliest_due_date = homeworks.earliest("due_date").due_date
        latest_due_date = homeworks.latest("due_date").due_date
        private_count = homeworks.only("private_to_user").filter(private_to_user=request.user).count()
        completed_count = homeworks \
            .only("userhomeworkrelation__completed") \
            .filter(userhomeworkrelation__completed=True) \
            .count()
        ignore_count = homeworks \
            .only("userhomeworkrelation__ignore") \
            .filter(userhomeworkrelation__ignore=True) \
            .count()
        type_set = set(homeworks.values_list("type", flat=True))
        type_set.discard(None)
        
        return Response({
            "due_date_min": earliest_due_date,
            "due_date_max": latest_due_date,
            "private_count": private_count,
            "types": list(type_set),
            "completed_count": completed_count,
            "ignore_count": ignore_count
        })
