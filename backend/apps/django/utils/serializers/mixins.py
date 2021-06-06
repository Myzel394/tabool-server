from rest_framework import serializers

__all__ = [
    "ValidationSerializer"
]


class ValidationSerializer(serializers.Serializer):
    """
    A serializer class which should only be used for validation. It doesn't provide a `create` or a `update`
    method.
    """

    def create(self, validated_data):
        name = self.__class__.__name__
        raise NotImplementedError(f"`create` shouldn't be used as `{name}` is only used for validation.")

    def update(self, instance, validated_data):
        name = self.__class__.__name__
        raise NotImplementedError(f"`update` shouldn't be used as `{name}` is only used for validation.")
