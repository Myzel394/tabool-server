from rest_framework import serializers

__all__ = [
    "GetHeadSerializer"
]


class GetHeadSerializer(serializers.Serializer):
    VALID_DOMAINS = ["bbb-schulen.rlp.net"]
    
    url = serializers.URLField()
    """
    def validate_url(self, instance: str) -> None:
        result: ParseResult = urlparse(instance)
        
        if result.netloc not in self.VALID_DOMAINS:
            raise ValidationError(f"Invalid domain. It must be one of {', '.join(self.VALID_DOMAINS)}")"""
