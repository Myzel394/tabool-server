from rest_framework import serializers

from apps.django.authentication.user.serializers import DetailUserSerializer
from ...models import News

__all__ = [
    "NewsListSerializer", "NewsDetailSerializer"
]


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "title", "created_at", "id"
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "title", "html", "author", "created_at", "edited_at", "id"
        ]

    author = DetailUserSerializer()
