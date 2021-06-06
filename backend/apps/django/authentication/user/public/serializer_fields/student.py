from apps.django.utils.serializers import WritableAllFieldMixin
from ...models import User

__all__ = [
    "StudentField"
]


class StudentField(WritableAllFieldMixin):
    model = User

    def to_internal_value(self, data):
        value = super().to_internal_value(data)

        if self.many:
            value = [
                user.student
                for user in value
            ]
        else:
            value = value.student

        return value
