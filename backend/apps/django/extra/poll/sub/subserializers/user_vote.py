from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...models import Choice
from ...public.serializer_fields import ChoiceField, PollField

__all__ = [
    "PollUserVoteSerializer"
]


class PollUserVoteSerializer(serializers.Serializer):
    poll = PollField()
    choices = ChoiceField(many=True)
    
    def validate(self, attrs):
        super().validate(attrs)
        
        poll = attrs["poll"]
        choices = attrs["choices"]
        choices_ids = [
            choice.id
            for choice in choices
        ]
        
        found_choices = Choice.objects.from_user(self.context["request"].user).filter(
            poll=poll,
            id__in=choices_ids
        )
        
        if found_choices.count() != len(choices):
            raise ValidationError({
                "choices": _("Diese Auswahlen sind nicht gültig.")
            })
        
        return attrs
