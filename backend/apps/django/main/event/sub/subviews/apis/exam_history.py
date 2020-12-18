from django_hint import *

from apps.django.utils.viewsets import ModelHistoryMixin, RetrieveFromUserMixin
from ....models import Exam
from ....serializers import ExamHistoryDetailSerializer, ExamHistoryListSerializer

__all__ = [
    "ExamHistoryViewSet"
]


class ExamHistoryViewSet(ModelHistoryMixin, RetrieveFromUserMixin):
    model = Exam
    
    def get_serializer_class(self):
        if self.action == "list":
            return ExamHistoryListSerializer
        return ExamHistoryDetailSerializer
    
    def get_obj_from_parent_qs(self, qs: QueryType) -> StandardModelType:
        return qs.only("pk").get(pk=self.kwargs["exam_pk"])
