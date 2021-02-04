from rest_framework import viewsets

from ....serializers import DetailTimetableSerializer

__all__ = [
    "TimetableViewSet"
]


class TimetableViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.RetrieveModelMixin
):
    serializer_class = DetailTimetableSerializer
