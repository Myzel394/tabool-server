from rest_framework import serializers

__all__ = {
    "DailyDataSerializer"
}


class DailyDataSerializer(serializers.Serializer):
    date = serializers.DateField()
    max_future_days = serializers.IntegerField(min_value=0, max_value=30)
