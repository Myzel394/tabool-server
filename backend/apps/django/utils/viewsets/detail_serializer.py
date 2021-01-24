from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

__all__ = [
    "DetailSerializerViewSetMixin"
]


class DetailSerializerViewSetMixin(viewsets.mixins.CreateModelMixin, viewsets.mixins.UpdateModelMixin):
    detail_serializer: serializers.Serializer
    serializer_action_map: dict[str, serializers.Serializer]
    
    def create(self, request, *args, **kwargs):
        # Super()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer) or serializer.instance
        
        headers = self.get_success_headers(serializer.data)
        
        # Return with detail serializer
        context = self.get_serializer_context()
        instance_serializer = self.detail_serializer(instance=instance, context=context)
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
        instance_serializer = self.detail_serializer(instance=instance, context=context)
        return Response(instance_serializer.data)
    
    def get_serializer_class(self):
        return self.serializer_action_map.get(self.action)
