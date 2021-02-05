from .base import BaseSubmissionSerializer

__all__ = [
    "UpdateSubmissionSerializer"
]


class UpdateSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "publish_datetime",
        ]
