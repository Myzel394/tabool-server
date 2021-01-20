from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...models import Choice, Vote
from ...public.serializer_fields.choice import ChoiceField
from ...public.serializer_fields.poll import PollField

__all__ = [
    "PollUserVoteSerializer"
]


class PollUserVoteSerializer(serializers.Serializer):
    poll = PollField()
    choices = ChoiceField(many=True)
    feedback = serializers.CharField(
        max_length=Vote._meta.get_field("feedback").max_length,
        allow_blank=True,
        allow_null=True,
        label=Vote._meta.get_field("feedback").max_length,
        required=False,
    )
    
    def validate(self, attrs):
        super().validate(attrs)
        
        # Choices
        poll = attrs["poll"]
        choices = attrs["choices"]
        choices_ids = [
            choice.id
            for choice in choices
        ]
        
        # Amount
        if not (poll.min_vote_choices <= len(choices_ids) <= poll.max_vote_choices):
            raise ValidationError({
                "choices": _(f"Wähle zwischen {poll.min_vote_choices} bis {poll.max_vote_choices} Elemente aus.")
            })
        
        found_choices = Choice.objects.from_user(self.context["request"].user).filter(
            poll=poll,
            id__in=choices_ids
        )
        
        if found_choices.count() != len(choices):
            raise ValidationError({
                "choices": _("Diese Auswahlen sind nicht gültig.")
            })
        
        return attrs
