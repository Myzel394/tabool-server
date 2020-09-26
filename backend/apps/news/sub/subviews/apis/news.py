from rest_framework import viewsets

from apps.utils.viewsets.mixins import RetrieveAllMixin
from ....models import News
from ....serializers import NewsDetailSerializer, NewsListSerializer

__all__ = [
    "NewsViewSet"
]


class NewsViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    model = News
    
    def get_serializer_class(self):
        if self.action == "list":
            return NewsListSerializer
        return NewsDetailSerializer
