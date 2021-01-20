from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .choice import ChoiceSerializer
from .user_vote import VoteSerializer
from ...models import Poll, Vote
from ...utils import get_results, has_voted

__all__ = [
    "PollSerializer"
]


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            "title", "created_at", "max_vote_date", "show_results_date", "max_vote_choices", "min_vote_choices",
            "id", "choices", "user_vote", "results"
        ]
    
    choices = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    
    def get_choices(self, instance: Poll):
        return ChoiceSerializer(instance.choices, many=True, context=self.context).data
    
    def get_user_vote(self, instance: Poll):
        user = self.context["request"].user
        
        try:
            vote = Vote.objects \
                .only("poll", "associated_user") \
                .get(poll=instance, associated_user=user)
        except ObjectDoesNotExist:
            return None
        
        return VoteSerializer(instance=vote).data
    
    def get_results(self, instance: Poll):
        if not settings.SHOW_VOTES_RESULTS:
            return None
        
        if not instance.show_results or not has_voted(poll=instance, user=self.context["request"].user):
            return None
        
        return get_results(instance=instance)
