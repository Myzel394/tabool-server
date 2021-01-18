from rest_framework import serializers

from ...models import Vote

__all__ = [
    "VoteSerializer"
]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["created_at", "choices", "id"]
    
    choices = serializers.SerializerMethodField()
    
    def get_choices(self, instance: Vote):
        return instance.choices.values_list("id", flat=True).distinct()
