from urllib.parse import ParseResult, urlparse

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.utils.serializers import ValidationSerializer

__all__ = [
    "GetPageTitleSerializer"
]


class GetPageTitleSerializer(ValidationSerializer):
    ALLOWED_DOMAINS = {"bbb-schulen.rlp.net"}
    ALLOWED_PROTOCOLS = {"https"}

    url = serializers.URLField()

    def validate_url(self, instance: str) -> None:
        result: ParseResult = urlparse(instance)

        if result.scheme not in self.ALLOWED_PROTOCOLS:
            raise ValidationError(f"Invalid protocol. It must be one of {', '.join(self.ALLOWED_PROTOCOLS)}")

        if result.netloc not in self.ALLOWED_DOMAINS:
            raise ValidationError(f"Invalid domain. It must be one of {', '.join(self.ALLOWED_DOMAINS)}")

        return instance
