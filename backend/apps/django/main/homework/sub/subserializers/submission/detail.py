from .base import BaseSubmissionSerializer
from ..material import DetailMaterialSerializer

__all__ = [
    "DetailSubmissionSerializer"
]


class DetailSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file", "id"
        ]
    
    lesson = DetailMaterialSerializer()
