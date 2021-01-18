from django.utils.translation import gettext_lazy as _
from django_hint import *
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ....models import Poll
from ....serializers import PollSerializer, PollUserVoteSerializer
from ....utils import add_user_vote, has_voted

__all__ = [
    "PollViewSet"
]


class PollViewSet(ReadOnlyModelViewSet):
    model = Poll
    serializer_class = PollSerializer
    
    def get_queryset(self):
        from_user = Poll.objects.from_user(self.request.user)
        if self.action in ["retrieve", "list"]:
            return from_user
        return from_user.not_voted(self.request.user)
    
    @action(["POST"], detail=True)
    def vote(self, request: RequestType, pk):
        # Validation
        data = request.data
        data.update({
            "poll": pk
        })
        
        serializer = PollUserVoteSerializer(data=data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        poll = validated_data["poll"]
        choices = validated_data["choices"]
        feedback = validated_data.get("feedback")
        user = request.user
        
        if has_voted(poll, user):
            return Response({
                "detail": _("Du hast bereits abgestimmt.")
            }, status=status.HTTP_423_LOCKED)
        
        add_user_vote(
            poll=poll,
            user=user,
            choices=choices,
            feedback=feedback
        )
        
        return Response(PollSerializer(instance=poll, context=self.get_serializer_context()).data)
