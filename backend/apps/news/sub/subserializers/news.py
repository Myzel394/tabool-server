from apps.authentication.sub.subserializers import UserDetailSerializer
from apps.utils.serializers import RandomIDSerializerMixin
from ...models import News

__all__ = [
    "NewsListSerializer", "NewsDetailSerializer"
]


class NewsListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = News
        fields = [
            "title", "created_at", "id"
        ]


class NewsDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = News
        fields = [
            "title", "html", "author", "created_at", "edited_at", "id"
        ]
    
    user = UserDetailSerializer()
