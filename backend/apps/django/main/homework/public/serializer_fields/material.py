from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Material

__all__ = [
    "MaterialField"
]


class MaterialField(WritableFromUserFieldMixin):
    model = Material
