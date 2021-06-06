from typing import *

from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from apps.django.authentication.user.constants import STUDENT, TEACHER

__all__ = [
    "DetailSerializerViewSetMixin"
]

Actions = Union["create", "update", "partial_update", "retrieve", "list", "delete"]
DetailSerializerType = dict[Union[STUDENT, TEACHER], serializers.Serializer]
SerializerActionsMap = dict[Actions, serializers.Serializer]
SerializerActionsMapPerType = dict[Union[STUDENT, TEACHER], SerializerActionsMap]


class DetailSerializerViewSetMixin(viewsets.GenericViewSet):
    detail_serializer: Union[DetailSerializerType, serializers.Serializer]
    serializer_action_map: Union[SerializerActionsMapPerType, SerializerActionsMap]

    def get_detail_serializer(self) -> serializers.Serializer:
        if type(self.detail_serializer) is dict:
            return self.detail_serializer[self.request.user.user_type]
        return self.detail_serializer

    def create(self, request, *args, **kwargs):
        # Super()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer) or serializer.instance

        headers = self.get_success_headers(serializer.data)

        # Return with detail serializer
        context = self.get_serializer_context()
        instance_serializer = self.get_detail_serializer()(instance=instance, context=context)
        return Response(instance_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # Super()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # Return with detail serializer
        context = self.get_serializer_context()
        instance_serializer = self.get_detail_serializer()(instance=instance, context=context)
        return Response(instance_serializer.data)

    def get_serializer_class(self):
        if any(value in self.serializer_action_map for value in {STUDENT, TEACHER}):
            # Is per type map
            per_type_map = self.serializer_action_map[self.request.user.user_type]

            return per_type_map.get(self.action, self.get_detail_serializer())

        # Is simple map
        return self.serializer_action_map.get(self.action, self.get_detail_serializer())
