from django_hint import *

from apps.django.main.homework.models import Homework
from apps.django.utils.viewsets.mixins import ModelHistoryMixin, RetrieveFromUserMixin
from ....serializers import HomeworkHistoryDetailSerializer, HomeworkHistoryListSerializer

__all__ = [
    "HomeworkHistoryViewSet"
]


class HomeworkHistoryViewSet(ModelHistoryMixin, RetrieveFromUserMixin):
    model = Homework
    
    def get_obj_from_parent_qs(self, qs: QueryType) -> StandardModelType:
        return qs.only("pk").get(pk=self.kwargs["homework_pk"])
    
    def get_serializer_class(self):
        if self.action == "list":
            return HomeworkHistoryListSerializer
        return HomeworkHistoryDetailSerializer
