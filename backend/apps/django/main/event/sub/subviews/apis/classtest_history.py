from django_hint import *

from apps.django.utils.viewsets import ModelHistoryMixin, RetrieveFromUserMixin
from ....models import Classtest
from ....serializers import ClasstestHistoryDetailSerializer, ClasstestHistoryListSerializer

__all__ = [
    "ClasstestHistoryViewSet"
]


class ClasstestHistoryViewSet(ModelHistoryMixin, RetrieveFromUserMixin):
    model = Classtest
    
    def get_serializer_class(self):
        if self.action == "list":
            return ClasstestHistoryListSerializer
        return ClasstestHistoryDetailSerializer
    
    def get_obj_from_parent_qs(self, qs: QueryType) -> StandardModelType:
        return qs.only("pk").get(pk=self.kwargs["classtest_pk"])
