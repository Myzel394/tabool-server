from urllib.parse import ParseResult, urlparse

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

__all__ = [
    "GetPageTitleSerializer"
]


class GetPageTitleSerializer(serializers.Serializer):
    VALID_DOMAINS = ["bbb-schulen.rlp.net"]

    url = serializers.URLField()

    def validate_url(self, instance: str) -> None:
        result: ParseResult = urlparse(instance)

        if result.netloc not in self.VALID_DOMAINS:
            raise ValidationError(f"Invalid domain. It must be one of {', '.join(self.VALID_DOMAINS)}")
