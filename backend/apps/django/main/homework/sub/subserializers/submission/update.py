from datetime import datetime
from typing import *

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .base import BaseSubmissionSerializer
from ....validators import only_future

if TYPE_CHECKING:
    from ....models import Submission

__all__ = [
    "UpdateSubmissionSerializer"
]


class UpdateSubmissionSerializer(BaseSubmissionSerializer):
    instance: "Submission"

    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "publish_datetime",
        ]

    publish_datetime = serializers.DateTimeField(
        required=False,
        allow_null=True,
        validators=[only_future]
    )

    def validate_publish_datetime(self, value: datetime):
        if self.instance.publish_datetime and self.instance.publish_datetime <= datetime.now():
            raise ValidationError(
                _("Diese Einsendung wurde bereits hochgeladen.")
            )

        return value
