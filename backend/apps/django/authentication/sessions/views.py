from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import SessionSerializer

__all__ = [
    "SessionViewSet"
]


class SessionViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin
):
    serializer_class = SessionSerializer
    
    def get_object(self):
        kwargs_name = self.lookup_url_kwarg or self.lookup_field
        pk = self.kwargs[kwargs_name]
        
        return get_object_or_404(
            self.get_queryset(),
            sessionrelation__id=pk
        )
    
    def get_queryset(self):
        return self.request.user.session_set.all()
