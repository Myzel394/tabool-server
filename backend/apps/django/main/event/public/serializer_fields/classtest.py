from apps.django.main.event.models import Classtest
from apps.django.main.event.sub.subserializers.classtest import ClasstestDetailSerializer
from apps.django.utils.serializers import WritableFromUserFieldMixin

__all__ = [
    "ClasstestField"
]


class ClasstestField(WritableFromUserFieldMixin):
    model = Classtest
    detail_serializer = ClasstestDetailSerializer
