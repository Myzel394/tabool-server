from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .choice import ChoiceSerializer
from ...models import Poll, Vote

__all__ = [
    "PollSerializer"
]


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            "title", "created_at", "max_vote_date", "show_results_date", "max_vote_choices", "id", "choices",
            "user_selections"
        ]
    
    choices = serializers.SerializerMethodField()
    user_selections = serializers.SerializerMethodField()
    
    def get_choices(self, instance: Poll):
        return ChoiceSerializer(instance.choices, many=True, context=self.context).data
    
    def get_user_selections(self, instance: Poll):
        user = self.context["request"].user
        
        try:
            vote = Vote.objects \
                .only("poll", "associated_user") \
                .get(poll=instance, associated_user=user)
        except ObjectDoesNotExist:
            return []
        
        return vote.choices \
            .values_list("id", flat=True) \
            .distinct()
