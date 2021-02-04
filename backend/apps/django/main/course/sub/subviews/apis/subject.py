from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from ....models import Course, Subject
from ....serializers import DetailSubjectSerializer

__all__ = [
    "SubjectViewSet"
]


class SubjectViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    serializer_class = DetailSubjectSerializer
    model = Subject
    ordering_fields = ["name", "short_name"]
    
    def get_queryset(self):
        subject_ids = Course.objects \
            .from_user(self.request.user) \
            .only("subject") \
            .values_list("subject", flat=True) \
            .distinct()
        subjects = Subject.objects.only("id").filter(id__in=subject_ids)
        
        return subjects
