from .base import BaseClassbookSerializer

__all__ = [
    "UpdateClassbookSerializer"
]


class UpdateClassbookSerializer(BaseClassbookSerializer):
    class Meta(BaseClassbookSerializer.Meta):
        fields = [
            "presence_content", "online_content", "video_conference_link"
        ]
